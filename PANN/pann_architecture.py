"""
Prime-Attentive Neural Network architecture implementation.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Tuple, List, Optional, Dict, Any


class PrimeEmbeddingLayer(nn.Module):
    """
    Maps input states to latent representation in prime space.
    """
    
    def __init__(
        self,
        input_dim: int,
        latent_dim: int,
        hidden_dim: int = 128,
        num_layers: int = 3
    ):
        super().__init__()
        
        self.input_dim = input_dim
        self.latent_dim = latent_dim
        
        # Encoder network
        layers = []
        current_dim = input_dim
        for i in range(num_layers):
            layers.append(nn.Linear(current_dim, hidden_dim))
            layers.append(nn.LayerNorm(hidden_dim))
            layers.append(nn.SiLU())
            current_dim = hidden_dim
        
        layers.append(nn.Linear(current_dim, latent_dim))
        self.encoder = nn.Sequential(*layers)
        
        # Learnable basis initialization
        self.prime_basis = nn.Parameter(
            torch.randn(latent_dim, latent_dim) * 0.1
        )
        
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Args:
            x: Input tensor of shape (batch_size, input_dim)
        
        Returns:
            z: Latent representation (batch_size, latent_dim)
            basis: Prime basis matrix (latent_dim, latent_dim)
        """
        z = self.encoder(x)
        
        # Orthogonalize basis for better conditioning
        with torch.no_grad():
            q, r = torch.linalg.qr(self.prime_basis)
            self.prime_basis.data = q
        
        return z, self.prime_basis


class PrimeFactorizationModule(nn.Module):
    """
    Factorizes latent representation into prime coefficients.
    """
    
    def __init__(
        self,
        latent_dim: int,
        num_primes: int,
        sparsity_weight: float = 0.01
    ):
        super().__init__()
        
        self.latent_dim = latent_dim
        self.num_primes = num_primes
        self.sparsity_weight = sparsity_weight
        
        # Factorization network
        self.factorizer = nn.Sequential(
            nn.Linear(latent_dim, latent_dim * 2),
            nn.LayerNorm(latent_dim * 2),
            nn.SiLU(),
            nn.Linear(latent_dim * 2, num_primes)
        )
        
        # Learnable prime multipliers (eigenvalues)
        self.prime_multipliers = nn.Parameter(
            torch.randn(num_primes, 2)  # Real and imaginary parts
        )
        
    def forward(
        self,
        z: torch.Tensor,
        basis: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Args:
            z: Latent representation (batch_size, latent_dim)
            basis: Prime basis matrix (latent_dim, latent_dim)
        
        Returns:
            coeffs: Prime coefficients (batch_size, num_primes)
            multipliers: Prime eigenvalues (num_primes,)
            sparsity_loss: Sparsity regularization term
        """
        # Get raw coefficients
        raw_coeffs = self.factorizer(z)
        
        # Apply soft thresholding for sparsity
        coeffs = F.softshrink(raw_coeffs, lambd=self.sparsity_weight)
        
        # Compute multipliers
        multipliers_real = self.prime_multipliers[:, 0]
        multipliers_imag = self.prime_multipliers[:, 1]
        multipliers = torch.complex(multipliers_real, multipliers_imag)
        
        # Sparsity loss
        sparsity_loss = torch.norm(coeffs, p=1, dim=-1).mean()
        
        return coeffs, multipliers, sparsity_loss


class PrimeEvolutionModule(nn.Module):
    """
    Models dynamics in prime coefficient space.
    """
    
    def __init__(
        self,
        num_primes: int,
        hidden_dim: int = 128,
        num_heads: int = 4
    ):
        super().__init__()
        
        self.num_primes = num_primes
        
        # Neural ODE for prime evolution
        self.prime_ode = nn.Sequential(
            nn.Linear(num_primes, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, num_primes)
        )
        
        # Attention for prime interactions
        self.attention = nn.MultiheadAttention(
            embed_dim=num_primes,
            num_heads=num_heads,
            batch_first=True
        )
        
        # Conservation regularization
        self.conservation_layer = nn.Linear(num_primes, 1)
        
    def forward(
        self,
        coeffs: torch.Tensor,
        multipliers: torch.Tensor,
        dt: float = 0.01,
        steps: int = 1
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Args:
            coeffs: Prime coefficients (batch_size, num_primes)
            multipliers: Prime eigenvalues (num_primes,)
            dt: Time step size
            steps: Number of integration steps
        
        Returns:
            coeffs_next: Evolved coefficients (batch_size, num_primes)
            conservation_loss: Conservation regularization term
        """
        batch_size = coeffs.shape[0]
        
        # Apply attention for prime interactions
        coeffs_reshaped = coeffs.unsqueeze(1)  # (batch, 1, num_primes)
        attn_output, _ = self.attention(
            coeffs_reshaped, coeffs_reshaped, coeffs_reshaped
        )
        coeffs = coeffs + 0.1 * attn_output.squeeze(1)
        
        # Neural ODE integration (Euler method)
        for _ in range(steps):
            # Get time derivative
            dcoeffs_dt = self.prime_ode(coeffs)
            
            # Apply eigenvalue-based scaling
            scale = torch.sigmoid(multipliers.real)
            dcoeffs_dt = dcoeffs_dt * scale.unsqueeze(0)
            
            # Euler step
            coeffs = coeffs + dt * dcoeffs_dt
        
        # Conservation loss (encourages invariant quantity)
        conserved = self.conservation_layer(coeffs)
        conservation_loss = torch.var(conserved)
        
        return coeffs, conservation_loss


class SymbolicDecoder(nn.Module):
    """
    Decodes prime representation to symbolic equations.
    """
    
    def __init__(
        self,
        num_primes: int,
        output_dim: int,
        max_terms: int = 10,
        vocab_size: int = 20
    ):
        super().__init__()
        
        self.num_primes = num_primes
        self.output_dim = output_dim
        self.max_terms = max_terms
        self.vocab_size = vocab_size
        
        # Operator vocabulary: +, *, sin, cos, exp, etc.
        self.operator_embeddings = nn.Embedding(vocab_size, num_primes)
        
        # Symbolic network
        self.symbolic_net = nn.Sequential(
            nn.Linear(num_primes, num_primes * 2),
            nn.LayerNorm(num_primes * 2),
            nn.SiLU(),
            nn.Linear(num_primes * 2, output_dim * max_terms * 3)  # coeff, power, op
        )
        
    def forward(
        self,
        coeffs: torch.Tensor,
        x: torch.Tensor
    ) -> Tuple[torch.Tensor, List[str]]:
        """
        Args:
            coeffs: Prime coefficients (batch_size, num_primes)
            x: Input state for symbolic evaluation (batch_size, output_dim)
        
        Returns:
            symbolic_output: Symbolic reconstruction (batch_size, output_dim)
            equations: List of equation strings
        """
        batch_size = coeffs.shape[0]
        
        # Generate symbolic parameters
        params = self.symbolic_net(coeffs)
        params = params.view(batch_size, self.output_dim, self.max_terms, 3)
        
        # Extract components
        coefficients = params[:, :, :, 0]  # (batch, output_dim, max_terms)
        exponents = params[:, :, :, 1]     # (batch, output_dim, max_terms)
        op_indices = params[:, :, :, 2].argmax(dim=-1)  # (batch, output_dim, max_terms)
        
        # Build symbolic expressions
        symbolic_output = torch.zeros(batch_size, self.output_dim).to(x.device)
        equations = []
        
        for i in range(batch_size):
            eq_str = []
            for j in range(self.output_dim):
                term_str = []
                total = 0.0
                
                for k in range(self.max_terms):
                    coeff = torch.sigmoid(coefficients[i, j, k])
                    exp = torch.tanh(exponents[i, j, k])
                    op_idx = op_indices[i, j, k]
                    
                    # Apply operator
                    if op_idx == 0:  # Linear term
                        term = coeff * (x[i, j] ** exp)
                        term_str.append(f"{coeff.item():.3f}*x{j}^{exp.item():.2f}")
                    elif op_idx == 1:  # Sine term
                        term = coeff * torch.sin(exp * x[i, j])
                        term_str.append(f"{coeff.item():.3f}*sin({exp.item():.2f}*x{j})")
                    elif op_idx == 2:  # Exponential term
                        term = coeff * torch.exp(exp * x[i, j])
                        term_str.append(f"{coeff.item():.3f}*exp({exp.item():.2f}*x{j})")
                    
                    total += term
                
                symbolic_output[i, j] = total
                eq_str.append(f"dx{j}/dt = " + " + ".join(term_str))
            
            equations.append("\n".join(eq_str))
        
        return symbolic_output, equations


class PrimeAttentiveNN(nn.Module):
    """
    Complete Prime-Attentive Neural Network.
    """
    
    def __init__(
        self,
        input_dim: int,
        latent_dim: int = 64,
        num_primes: int = 32,
        output_dim: Optional[int] = None,
        hidden_dim: int = 128,
        sparsity_weight: float = 0.01,
        conservation_weight: float = 0.1
    ):
        super().__init__()
        
        if output_dim is None:
            output_dim = input_dim
        
        self.input_dim = input_dim
        self.latent_dim = latent_dim
        self.num_primes = num_primes
        self.output_dim = output_dim
        self.sparsity_weight = sparsity_weight
        self.conservation_weight = conservation_weight
        
        # Components
        self.embedding = PrimeEmbeddingLayer(
            input_dim=input_dim,
            latent_dim=latent_dim,
            hidden_dim=hidden_dim
        )
        
        self.factorization = PrimeFactorizationModule(
            latent_dim=latent_dim,
            num_primes=num_primes,
            sparsity_weight=sparsity_weight
        )
        
        self.evolution = PrimeEvolutionModule(
            num_primes=num_primes,
            hidden_dim=hidden_dim
        )
        
        self.decoder = nn.Sequential(
            nn.Linear(num_primes, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, output_dim)
        )
        
        self.symbolic_decoder = SymbolicDecoder(
            num_primes=num_primes,
            output_dim=output_dim
        )
        
    def forward(
        self,
        x: torch.Tensor,
        dt: float = 0.01,
        return_symbolic: bool = False
    ) -> Dict[str, Any]:
        """
        Forward pass of the complete PANN.
        
        Args:
            x: Input state (batch_size, input_dim)
            dt: Time step for evolution
            return_symbolic: Whether to return symbolic equations
        
        Returns:
            Dictionary containing all outputs and intermediate states
        """
        batch_size = x.shape[0]
        
        # 1. Embed to latent space
        z, basis = self.embedding(x)
        
        # 2. Factorize into primes
        coeffs, multipliers, sparsity_loss = self.factorization(z, basis)
        
        # 3. Evolve primes
        coeffs_next, conservation_loss = self.evolution(
            coeffs, multipliers, dt=dt
        )
        
        # 4. Decode to state space
        x_pred = self.decoder(coeffs_next)
        
        # 5. Optional symbolic decoding
        symbolic_output = None
        equations = []
        if return_symbolic:
            symbolic_output, equations = self.symbolic_decoder(coeffs, x)
        
        # Orthogonality loss (encourage orthogonal prime basis)
        ortho_loss = torch.norm(
            basis @ basis.T - torch.eye(self.latent_dim).to(x.device),
            p='fro'
        )
        
        # Total regularization loss
        reg_loss = (
            self.sparsity_weight * sparsity_loss +
            self.conservation_weight * conservation_loss +
            0.01 * ortho_loss
        )
        
        return {
            'x_pred': x_pred,
            'z': z,
            'coeffs': coeffs,
            'coeffs_next': coeffs_next,
            'multipliers': multipliers,
            'basis': basis,
            'symbolic_output': symbolic_output,
            'equations': equations,
            'sparsity_loss': sparsity_loss,
            'conservation_loss': conservation_loss,
            'ortho_loss': ortho_loss,
            'reg_loss': reg_loss
        }
    
    def extract_primes(self) -> List[Dict[str, Any]]:
        """
        Extract learned primes as interpretable components.
        
        Returns:
            List of dictionaries describing each prime
        """
        primes = []
        
        # Get multipliers (eigenvalues)
        multipliers = self.factorization.prime_multipliers
        eigenvalues = torch.complex(
            multipliers[:, 0],
            multipliers[:, 1]
        ).detach().cpu().numpy()
        
        # Get basis vectors (approximate eigenfunctions)
        basis = self.embedding.prime_basis.detach().cpu().numpy()
        
        for i in range(self.num_primes):
            prime_info = {
                'index': i,
                'eigenvalue': eigenvalues[i],
                'eigenvector': basis[:, i],
                'lyapunov_exponent': np.log(abs(eigenvalues[i])),
                'frequency': np.angle(eigenvalues[i]),
                'importance': np.mean(np.abs(
                    self.factorization.factorizer[-1].weight[i].detach().cpu().numpy()
                ))
            }
            primes.append(prime_info)
        
        return primes