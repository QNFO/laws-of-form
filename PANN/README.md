# Prime-Attentive Neural Networks (PANNs)

A framework for interpretable decomposition of chaotic dynamical systems into fundamental "prime" components.

## Overview

This repository implements **Prime-Attentive Neural Networks (PANNs)** – a novel neural architecture that decomposes chaotic systems into irreducible components called *dynamical primes*. Each prime represents a fundamental mode of the system with its own eigenvalue (growth/oscillation rate), eigenfunction (spatial pattern), and topological signature.

Key features:
- **Mathematically grounded** in spectral theory of dynamical systems
- **Interpretable by design** with symbolic equation extraction
- **Topologically consistent** using persistent homology regularization
- **Validated** on canonical chaotic systems (Lorenz, logistic map)

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/pann.git
cd pann

# Install dependencies
pip install -r requirements.txt

# Optional: Install PyTorch with CUDA support
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

## Quick Start

### Run Lorenz Experiment
```bash
python main.py --experiment lorenz --num_epochs 200 --visualize
```

### Run Logistic Map Experiments
```bash
python main.py --experiment logistic --r_values 3.5 3.7 3.9 4.0 --visualize
```

### Train Custom Model
```python
from pann_architecture import PrimeAttentiveNN
from training import PANNTrainer

# Create model
model = PrimeAttentiveNN(
    input_dim=3,      # Lorenz system has 3 dimensions
    latent_dim=64,    # Size of latent space
    num_primes=16,    # Number of dynamical primes
    hidden_dim=128
)

# Create trainer and train
trainer = PANNTrainer(model, learning_rate=1e-3)
trainer.train(train_loader, val_loader, num_epochs=200)
```

## Architecture

The PANN consists of four main components:

1. **Prime Embedding Layer**: Maps state space to structured latent space
2. **Factorization Module**: Decomposes latent representation into prime coefficients
3. **Prime Evolution Module**: Models dynamics in prime space
4. **Symbolic Decoder**: Extracts human-readable equations from prime representation

## Mathematical Foundations

### Dynamical Primes
A *dynamical prime* is defined as a triple:
- **Invariant submanifold**: Minimal invariant set
- **Ergodic measure**: Natural measure on the submanifold  
- **Koopman eigenfunction**: Eigenfunction of the Koopman operator with eigenvalue λ

### Prime Continuum
The set of all dynamical primes forms a *prime continuum* – a measurable space indexing the irreducible components of the system.

### Key Theorems
1. **Prime Decomposition**: Chaotic systems admit decomposition into primes
2. **Spectral Correspondence**: Primes correspond to Koopman eigenmodes
3. **Topological Consistency**: Each prime has associated persistent homology barcode

## Examples

### Logistic Map Bifurcation
```python
# Analyze Feigenbaum scaling
from experiments import analyze_feigenbaum_scaling
analysis = analyze_feigenbaum_scaling(logistic_results)
print(f"Estimated δ: {analysis['feigenbaum_estimate']:.3f}")
# Expected: ≈ 4.669
```

### Symbolic Equation Extraction
```python
# Get interpretable equations
outputs = model(x, return_symbolic=True)
for eq in outputs['equations'][:3]:
    print(eq)
# Example output:
# dx0/dt = 0.142*sin(1.832*x0) + 0.083*exp(0.512*x1)
# dx1/dt = -0.234*x0 + 0.167*x0*x1
```

### Topological Validation
```python
from topological_regularization import analyze_topological_invariants

# Analyze topology of learned attractor
topology = analyze_topological_invariants(trajectory, prime_coeffs)
print(f"Betti numbers: {topology['betti_numbers']}")
# Expected for Lorenz: β₀=1, β₁=2 (double loop)
```

## Applications

1. **Climate Science**: Decompose ENSO into fundamental modes
2. **Plasma Physics**: Identify coherent structures in turbulence  
3. **Neuroscience**: Decompose neural dynamics into functional modules
4. **Financial Systems**: Identify fundamental market regimes

## Research References

### Theoretical Foundations
- Koopman operator theory
- Ergodic decomposition theorems  
- Persistent homology in dynamical systems
- Spectral theory of chaotic systems

### Related Work
- SINDy: Sparse Identification of Nonlinear Dynamics
- Neural ODEs: Continuous-depth models
- Reservoir Computing: Echo state networks
- Dynamic Mode Decomposition (DMD)
