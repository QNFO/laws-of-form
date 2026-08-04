"""
Mathematical definitions and operations for the prime continuum concept.
Defines dynamical primes and their properties.
"""
import numpy as np
from typing import Tuple, Optional, Dict, Any
from dataclasses import dataclass
from scipy import sparse
from scipy.sparse.linalg import eigs

@dataclass
class DynamicalPrime:
    """Represents a dynamical prime component."""
    eigenvalue: complex  # λ_α - growth/oscillation rate
    eigenfunction: np.ndarray  # φ_α - pattern in state space
    measure: np.ndarray  # ν_α - ergodic measure
    topological_invariant: Dict[str, Any]  # Barcode/persistence info
    physical_interpretation: str  # Human-readable description
    
    @property
    def lyapunov_exponent(self) -> float:
        """Compute Lyapunov exponent from eigenvalue."""
        return np.log(abs(self.eigenvalue))
    
    @property
    def frequency(self) -> float:
        """Compute oscillation frequency from eigenvalue."""
        return np.angle(self.eigenvalue)
    
    @property
    def persistence_length(self) -> float:
        """Length of topological persistence interval."""
        if 'lifetime' in self.topological_invariant:
            return self.topological_invariant['lifetime']
        return 1.0 / max(abs(self.lyapunov_exponent), 1e-10)


class PrimeContinuum:
    """Represents a continuum of dynamical primes."""
    
    def __init__(self, dimension: int, num_primes: int = 32):
        self.dimension = dimension  # Dimension of state space
        self.num_primes = num_primes
        self.primes = []  # List of DynamicalPrime objects
        self.continuum_measure = None  # Measure on the continuum
        
    def add_prime(self, prime: DynamicalPrime):
        """Add a prime to the continuum."""
        self.primes.append(prime)
        
    def spectral_decomposition(self, f: np.ndarray) -> np.ndarray:
        """Decompose function f into prime components."""
        if not self.primes:
            raise ValueError("No primes in continuum")
            
        coefficients = np.zeros(len(self.primes), dtype=complex)
        for i, prime in enumerate(self.primes):
            # Project f onto prime eigenfunction
            coefficients[i] = np.vdot(prime.eigenfunction, f)
            
        return coefficients
    
    def reconstruct(self, coefficients: np.ndarray) -> np.ndarray:
        """Reconstruct function from prime components."""
        reconstruction = np.zeros(self.dimension, dtype=complex)
        for i, prime in enumerate(self.primes):
            reconstruction += coefficients[i] * prime.eigenfunction
        return reconstruction
    
    def prime_metric(self, alpha: int, beta: int) -> float:
        """Compute distance between two primes."""
        if alpha >= len(self.primes) or beta >= len(self.primes):
            raise ValueError("Prime indices out of range")
            
        p1 = self.primes[alpha]
        p2 = self.primes[beta]
        
        # Distance in eigenvalue space
        eig_dist = abs(p1.eigenvalue - p2.eigenvalue)
        
        # Distance in eigenfunction space (cosine distance)
        func_dist = 1 - abs(np.vdot(p1.eigenfunction, p2.eigenfunction))
        
        # Combined metric
        return 0.7 * eig_dist + 0.3 * func_dist
    
    def get_koopman_operator(self) -> sparse.csr_matrix:
        """Construct finite approximation of Koopman operator from primes."""
        n = len(self.primes)
        if n == 0:
            return sparse.csr_matrix((0, 0))
            
        # Koopman operator is diagonal in prime basis
        data = np.array([p.eigenvalue for p in self.primes])
        indices = np.arange(n)
        indptr = np.arange(n + 1)
        
        return sparse.csr_matrix((data, indices, indices), shape=(n, n))
    
    def feigenbaum_ratio(self, period_doubling: bool = True) -> Optional[float]:
        """Estimate Feigenbaum constant from prime scaling."""
        if len(self.primes) < 2:
            return None
            
        if period_doubling:
            # Look for period-doubling sequence in eigenvalues
            eigenvalues = [p.eigenvalue for p in self.primes]
            magnitudes = [abs(eig) for eig in eigenvalues]
            magnitudes.sort()
            
            if len(magnitudes) >= 3:
                ratios = []
                for i in range(len(magnitudes) - 2):
                    if magnitudes[i] > 0:
                        ratio = (magnitudes[i+1] - magnitudes[i]) / \
                                (magnitudes[i+2] - magnitudes[i+1])
                        ratios.append(ratio)
                
                if ratios:
                    return np.mean(ratios)
        
        return None


def extract_primes_from_koopman(
    koopman_matrix: np.ndarray,
    state_dimension: int,
    num_primes: Optional[int] = None
) -> PrimeContinuum:
    """
    Extract dynamical primes from empirical Koopman operator.
    
    Args:
        koopman_matrix: Empirical Koopman operator (n x n)
        state_dimension: Dimension of original state space
        num_primes: Number of primes to extract (default: all)
    
    Returns:
        PrimeContinuum object containing extracted primes
    """
    n = koopman_matrix.shape[0]
    if num_primes is None:
        num_primes = min(20, n)
    
    # Compute eigenvalues and eigenvectors
    eigenvalues, eigenvectors = eigs(
        koopman_matrix, 
        k=num_primes, 
        which='LM'  # Largest magnitude
    )
    
    # Create continuum
    continuum = PrimeContinuum(
        dimension=state_dimension,
        num_primes=num_primes
    )
    
    # Create prime objects
    for i in range(num_primes):
        # Project eigenvector back to state space
        # (In practice, this would use reconstruction from observables)
        eigenfunction = eigenvectors[:, i]
        
        prime = DynamicalPrime(
            eigenvalue=eigenvalues[i],
            eigenfunction=eigenfunction,
            measure=np.abs(eigenfunction)**2,  # Born rule analogy
            topological_invariant={
                'lifetime': 1.0 / max(abs(np.log(abs(eigenvalues[i]))), 1e-10)
            },
            physical_interpretation=f"Prime {i}: λ={eigenvalues[i]:.3f}"
        )
        
        continuum.add_prime(prime)
    
    return continuum