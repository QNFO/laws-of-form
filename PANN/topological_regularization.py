"""
Topological Data Analysis integration for regularization and validation.
Uses persistent homology to ensure topological consistency of learned primes.
"""
import numpy as np
import torch
import torch.nn as nn
from typing import List, Tuple, Dict, Any, Optional
from scipy.spatial.distance import pdist, squareform

try:
    import gudhi as gd
    GUDHI_AVAILABLE = True
except ImportError:
    GUDHI_AVAILABLE = False
    print("Warning: Gudhi not available. Using mock topological computations.")


class TopologicalRegularizer:
    """
    Computes topological regularization terms for PANN training.
    """
    
    def __init__(
        self,
        homology_dimensions: List[int] = None,
        persistence_weight: float = 0.1,
        consistency_weight: float = 0.05
    ):
        if homology_dimensions is None:
            homology_dimensions = [0, 1]  # Connected components and loops
        
        self.homology_dimensions = homology_dimensions
        self.persistence_weight = persistence_weight
        self.consistency_weight = consistency_weight
        
        if not GUDHI_AVAILABLE:
            print("Warning: Running without actual TDA computations.")
    
    def compute_persistence(
        self,
        points: np.ndarray,
        max_edge_length: float = 1.0
    ) -> Dict[int, List[Tuple[float, float]]]:
        """
        Compute persistent homology of point cloud.
        
        Args:
            points: Point cloud (n_points, n_dimensions)
            max_edge_length: Maximum edge length for filtration
        
        Returns:
            Dictionary mapping homology dimension to list of (birth, death) pairs
        """
        if not GUDHI_AVAILABLE or len(points) < 3:
            # Return mock persistence for testing
            return {dim: [(0.1, 0.5), (0.2, 0.8)] for dim in self.homology_dimensions}
        
        # Compute Vietoris-Rips complex
        rips = gd.RipsComplex(points=points, max_edge_length=max_edge_length)
        simplex_tree = rips.create_simplex_tree(max_dimension=max(self.homology_dimensions) + 1)
        
        # Compute persistence
        persistence = simplex_tree.persistence()
        
        # Organize by dimension
        persistence_by_dim = {dim: [] for dim in self.homology_dimensions}
        for (dim, (birth, death)) in persistence:
            if dim in persistence_by_dim:
                if death == float('inf'):
                    death = max_edge_length * 2  # Handle infinite persistence
                persistence_by_dim[dim].append((birth, death))
        
        return persistence_by_dim
    
    def persistence_loss(
        self,
        predicted_points: torch.Tensor,
        true_points: torch.Tensor
    ) -> torch.Tensor:
        """
        Compute loss based on persistence diagram similarity.
        
        Args:
            predicted_points: Predicted trajectory points
            true_points: True trajectory points
        
        Returns:
            Persistence matching loss
        """
        if not GUDHI_AVAILABLE:
            # Mock loss when TDA not available
            return torch.tensor(0.0).to(predicted_points.device)
        
        # Convert to numpy for TDA computation
        pred_np = predicted_points.detach().cpu().numpy()
        true_np = true_points.detach().cpu().numpy()
        
        # Compute persistence diagrams
        pred_persistence = self.compute_persistence(pred_np)
        true_persistence = self.compute_persistence(true_np)
        
        # Compute Wasserstein distance between diagrams
        total_loss = 0.0
        
        for dim in self.homology_dimensions:
            pred_pairs = pred_persistence.get(dim, [])
            true_pairs = true_persistence.get(dim, [])
            
            if not pred_pairs and not true_pairs:
                continue
            
            # Create persistence diagrams
            pred_diag = np.array(pred_pairs) if pred_pairs else np.zeros((0, 2))
            true_diag = np.array(true_pairs) if true_pairs else np.zeros((0, 2))
            
            # Pad diagrams to same size
            max_len = max(len(pred_diag), len(true_diag))
            if len(pred_diag) < max_len:
                pred_diag = np.vstack([pred_diag, np.zeros((max_len - len(pred_diag), 2))])
            if len(true_diag) < max_len:
                true_diag = np.vstack([true_diag, np.zeros((max_len - len(true_diag), 2))])
            
            # Compute Wasserstein distance (approximate)
            wasserstein_dist = np.sqrt(np.mean((pred_diag - true_diag) ** 2))
            total_loss += wasserstein_dist
        
        return torch.tensor(total_loss).to(predicted_points.device)
    
    def topological_consistency_loss(
        self,
        prime_coeffs: torch.Tensor,
        multipliers: torch.Tensor
    ) -> torch.Tensor:
        """
        Ensure topological consistency between primes.
        Primes with similar eigenvalues should have similar topological signatures.
        
        Args:
            prime_coeffs: Prime coefficients
            multipliers: Prime eigenvalues
        
        Returns:
            Topological consistency loss
        """
        # Compute similarity matrix from eigenvalues
        eig_similarity = torch.cdist(
            multipliers.real.unsqueeze(1),
            multipliers.real.unsqueeze(1)
        )
        
        # Compute similarity matrix from coefficient patterns
        coeff_similarity = torch.cdist(prime_coeffs.T, prime_coeffs.T)
        
        # Normalize
        eig_similarity = eig_similarity / (eig_similarity.max() + 1e-10)
        coeff_similarity = coeff_similarity / (coeff_similarity.max() + 1e-10)
        
        # Consistency loss: eigenvalues and coefficients should give similar similarity
        consistency_loss = torch.norm(eig_similarity - coeff_similarity, p='fro')
        
        return consistency_loss
    
    def prime_barcode_loss(
        self,
        multipliers: torch.Tensor,
        target_lifetimes: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """
        Regularize prime lifetimes (barcode lengths) to match expected distribution.
        
        Args:
            multipliers: Prime eigenvalues
            target_lifetimes: Target barcode lengths (optional)
        
        Returns:
            Barcode regularization loss
        """
        # Compute lifetimes from eigenvalues
        lifetimes = 1.0 / torch.clamp(torch.abs(torch.log(torch.abs(multipliers))), min=1e-5)
        
        if target_lifetimes is not None:
            # Match target distribution
            lifetime_loss = torch.norm(lifetimes - target_lifetimes, p=2)
        else:
            # Encourage diverse lifetimes
            lifetime_var = torch.var(lifetimes)
            # Want some variation but not extreme
            target_var = torch.tensor(1.0).to(lifetimes.device)
            lifetime_loss = torch.abs(lifetime_var - target_var)
        
        return lifetime_loss
    
    def __call__(
        self,
        predicted_trajectory: torch.Tensor,
        true_trajectory: torch.Tensor,
        prime_coeffs: torch.Tensor,
        multipliers: torch.Tensor,
        target_lifetimes: Optional[torch.Tensor] = None
    ) -> Dict[str, torch.Tensor]:
        """
        Compute all topological regularization losses.
        
        Returns:
            Dictionary of loss components
        """
        losses = {}
        
        # Persistence matching loss
        losses['persistence'] = self.persistence_loss(
            predicted_trajectory, true_trajectory
        )
        
        # Topological consistency loss
        losses['consistency'] = self.topological_consistency_loss(
            prime_coeffs, multipliers
        )
        
        # Barcode regularization
        losses['barcode'] = self.prime_barcode_loss(
            multipliers, target_lifetimes
        )
        
        # Weighted total
        losses['total'] = (
            self.persistence_weight * losses['persistence'] +
            self.consistency_weight * losses['consistency'] +
            0.01 * losses['barcode']
        )
        
        return losses


class TopologyAwareLoss(nn.Module):
    """
    Combined loss function with topological regularization.
    """
    
    def __init__(
        self,
        prediction_weight: float = 1.0,
        topological_weight: float = 0.1,
        sparsity_weight: float = 0.01,
        conservation_weight: float = 0.05
    ):
        super().__init__()
        
        self.prediction_weight = prediction_weight
        self.topological_weight = topological_weight
        self.sparsity_weight = sparsity_weight
        self.conservation_weight = conservation_weight
        
        # Base losses
        self.mse_loss = nn.MSELoss()
        self.topological_regularizer = TopologicalRegularizer()
        
    def forward(
        self,
        predictions: Dict[str, Any],
        targets: torch.Tensor,
        true_trajectory: Optional[torch.Tensor] = None
    ) -> Dict[str, torch.Tensor]:
        """
        Compute combined loss.
        
        Args:
            predictions: Output from PANN.forward()
            targets: Target states
            true_trajectory: Full true trajectory for topological comparison
        
        Returns:
            Dictionary of loss components
        """
        losses = {}
        
        # Prediction loss
        losses['prediction'] = self.mse_loss(predictions['x_pred'], targets)
        
        # Topological loss (if trajectory available)
        if true_trajectory is not None:
            topo_losses = self.topological_regularizer(
                predicted_trajectory=predictions['x_pred'],
                true_trajectory=true_trajectory,
                prime_coeffs=predictions['coeffs'],
                multipliers=predictions['multipliers']
            )
            losses.update({f'topo_{k}': v for k, v in topo_losses.items()})
        else:
            losses['topo_total'] = torch.tensor(0.0).to(targets.device)
        
        # Regularization losses from PANN
        losses['sparsity'] = predictions.get('sparsity_loss', torch.tensor(0.0))
        losses['conservation'] = predictions.get('conservation_loss', torch.tensor(0.0))
        losses['ortho'] = predictions.get('ortho_loss', torch.tensor(0.0))
        
        # Combined total loss
        losses['total'] = (
            self.prediction_weight * losses['prediction'] +
            self.topological_weight * losses.get('topo_total', torch.tensor(0.0)) +
            self.sparsity_weight * losses['sparsity'] +
            self.conservation_weight * losses['conservation'] +
            0.001 * losses['ortho']
        )
        
        return losses


def compute_betti_numbers(
    points: np.ndarray,
    threshold: float = 0.5
) -> Dict[int, int]:
    """
    Compute Betti numbers at given threshold.
    
    Args:
        points: Point cloud
        threshold: Distance threshold
    
    Returns:
        Dictionary of Betti numbers by dimension
    """
    if not GUDHI_AVAILABLE or len(points) < 3:
        return {0: 1, 1: 1}  # Mock values
    
    # Create Vietoris-Rips complex
    rips = gd.RipsComplex(points=points, max_edge_length=threshold)
    simplex_tree = rips.create_simplex_tree(max_dimension=2)
    
    # Compute Betti numbers
    betti_numbers = {}
    for dim in [0, 1]:
        betti_numbers[dim] = simplex_tree.betti_numbers()[dim]
    
    return betti_numbers


def analyze_topological_invariants(
    trajectory: np.ndarray,
    prime_coeffs: np.ndarray
) -> Dict[str, Any]:
    """
    Analyze topological invariants of trajectory and prime decomposition.
    
    Args:
        trajectory: Time series data
        prime_coeffs: Prime coefficients
    
    Returns:
        Dictionary of topological analysis results
    """
    results = {}
    
    # Analyze trajectory topology
    if len(trajectory) > 10:
        persistence = TopologicalRegularizer().compute_persistence(trajectory)
        results['trajectory_persistence'] = persistence
        
        # Compute Betti numbers at median distance
        distances = pdist(trajectory)
        median_dist = np.median(distances)
        results['betti_numbers'] = compute_betti_numbers(trajectory, median_dist)
    
    # Analyze prime coefficient topology
    if prime_coeffs.shape[1] > 1:
        # Project to 2D for visualization
        from sklearn.decomposition import PCA
        pca = PCA(n_components=2)
        coeffs_2d = pca.fit_transform(prime_coeffs)
        
        prime_persistence = TopologicalRegularizer().compute_persistence(coeffs_2d)
        results['prime_persistence'] = prime_persistence
    
    return results