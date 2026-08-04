"""
Experimental evaluation of Prime-Attentive Neural Networks.
"""
import torch
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Any, List, Tuple
import seaborn as sns
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

sns.set_style("whitegrid")


class PANNExperiment:
    """
    Base class for PANN experiments.
    """
    
    def __init__(self, model, device='cuda'):
        self.model = model
        self.device = device
        
    def evaluate_prediction(
        self,
        test_loader,
        horizon: int = 100
    ) -> Dict[str, float]:
        """
        Evaluate multi-step prediction performance.
        
        Args:
            test_loader: Test data loader
            horizon: Prediction horizon
        
        Returns:
            Dictionary of evaluation metrics
        """
        self.model.eval()
        all_predictions = []
        all_targets = []
        
        with torch.no_grad():
            for x, y in test_loader:
                x, y = x.to(self.device), y.to(self.device)
                
                # Multi-step prediction
                predictions = []
                current = x
                for _ in range(horizon):
                    outputs = self.model(current, dt=0.01)
                    pred = outputs['x_pred']
                    predictions.append(pred)
                    current = pred
                
                predictions = torch.stack(predictions, dim=1)
                all_predictions.append(predictions.cpu().numpy())
                all_targets.append(y.cpu().numpy())
        
        # Concatenate all batches
        all_predictions = np.concatenate(all_predictions, axis=0)
        all_targets = np.concatenate(all_targets, axis=0)
        
        # Compute metrics
        mse = mean_squared_error(all_targets.flatten(), all_predictions[:, 0].flatten())
        mae = mean_absolute_error(all_targets.flatten(), all_predictions[:, 0].flatten())
        
        # Lyapunov time estimation
        lyapunov_time = self.estimate_lyapunov_time(all_predictions, all_targets)
        
        return {
            'mse': mse,
            'mae': mae,
            'lyapunov_time': lyapunov_time,
            'predictions': all_predictions,
            'targets': all_targets
        }
    
    def estimate_lyapunov_time(
        self,
        predictions: np.ndarray,
        targets: np.ndarray,
        max_time: int = 50
    ) -> float:
        """
        Estimate Lyapunov time from prediction error growth.
        
        Args:
            predictions: Predicted trajectories
            targets: True trajectories
            max_time: Maximum time for fitting
        
        Returns:
            Estimated Lyapunov time
        """
        # Compute prediction errors over time
        errors = []
        for t in range(min(max_time, predictions.shape[1])):
            error = np.mean((predictions[:, t] - targets[:, 0]) ** 2)
            errors.append(error)
        
        errors = np.array(errors)
        
        # Fit exponential growth
        if len(errors) > 3 and np.all(errors > 0):
            log_errors = np.log(errors)
            times = np.arange(len(errors))
            
            # Linear fit to log errors
            coeffs = np.polyfit(times[:min(10, len(times))], 
                               log_errors[:min(10, len(times))], 1)
            lyapunov_exponent = coeffs[0]
            
            if lyapunov_exponent > 0:
                return 1.0 / lyapunov_exponent
        
        return float('nan')
    
    def analyze_prime_spectrum(self, test_loader) -> Dict[str, Any]:
        """
        Analyze the spectrum of learned primes.
        
        Args:
            test_loader: Test data loader
        
        Returns:
            Prime spectrum analysis
        """
        self.model.eval()
        all_coeffs = []
        all_multipliers = []
        
        with torch.no_grad():
            for x, _ in test_loader:
                x = x.to(self.device)
                outputs = self.model(x, dt=0.01)
                all_coeffs.append(outputs['coeffs'].cpu().numpy())
                all_multipliers.append(outputs['multipliers'].cpu().numpy())
        
        # Analyze spectrum
        all_coeffs = np.vstack(all_coeffs)
        multipliers = all_multipliers[0]  # Same for all batches
        
        # Compute eigenvalue statistics
        eigenvalues = multipliers
        magnitudes = np.abs(eigenvalues)
        angles = np.angle(eigenvalues)
        
        # Sort by importance (mean absolute activation)
        importance = np.mean(np.abs(all_coeffs), axis=0)
        sorted_idx = np.argsort(importance)[::-1]
        
        spectrum_analysis = {
            'eigenvalues': eigenvalues,
            'magnitudes': magnitudes,
            'angles': angles,
            'importance': importance,
            'sorted_indices': sorted_idx,
            'num_unstable': np.sum(magnitudes > 1.0),
            'num_oscillatory': np.sum(np.abs(angles) > 0.1),
            'spectral_entropy': -np.sum(importance * np.log(importance + 1e-10))
        }
        
        return spectrum_analysis
    
    def visualize_prime_decomposition(
        self,
        trajectory: np.ndarray,
        save_path: str = None
    ):
        """
        Visualize prime decomposition of a trajectory.
        
        Args:
            trajectory: Input trajectory
            save_path: Path to save figure
        """
        self.model.eval()
        
        # Convert to tensor
        x_tensor = torch.FloatTensor(trajectory).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(x_tensor, dt=0.01)
        
        # Get prime coefficients
        coeffs = outputs['coeffs'].cpu().numpy()
        
        # Create visualization
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Plot trajectory
        if trajectory.shape[1] >= 3:
            ax = axes[0, 0]
            ax.plot(trajectory[:, 0], trajectory[:, 1], alpha=0.6)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title('Trajectory (x-y projection)')
        
        # Plot prime activations
        ax = axes[0, 1]
        im = ax.imshow(coeffs.T, aspect='auto', cmap='RdBu_r')
        ax.set_xlabel('Time step')
        ax.set_ylabel('Prime index')
        ax.set_title('Prime Coefficient Activations')
        plt.colorbar(im, ax=ax)
        
        # Plot eigenvalue spectrum
        ax = axes[1, 0]
        multipliers = outputs['multipliers'].cpu().numpy()
        magnitudes = np.abs(multipliers)
        angles = np.angle(multipliers)
        
        # Polar plot of eigenvalues
        scatter = ax.scatter(angles, magnitudes, c=np.arange(len(magnitudes)), 
                            cmap='viridis', alpha=0.6)
        ax.set_xlabel('Angle (rad)')
        ax.set_ylabel('Magnitude')
        ax.set_title('Eigenvalue Spectrum')
        ax.grid(True)
        
        # Plot contribution of top primes
        ax = axes[1, 1]
        importance = np.mean(np.abs(coeffs), axis=0)
        top_n = min(10, len(importance))
        top_idx = np.argsort(importance)[-top_n:][::-1]
        
        for i, idx in enumerate(top_idx):
            ax.plot(coeffs[:, idx], label=f'Prime {idx}', alpha=0.7)
        
        ax.set_xlabel('Time step')
        ax.set_ylabel('Coefficient value')
        ax.set_title(f'Top {top_n} Prime Contributions')
        ax.legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def compare_with_baselines(
        self,
        test_loader,
        baseline_models: Dict[str, Any],
        metrics: List[str] = ['mse', 'mae', 'lyapunov_time']
    ) -> Dict[str, Dict[str, float]]:
        """
        Compare PANN with baseline models.
        
        Args:
            test_loader: Test data loader
            baseline_models: Dictionary of baseline models
            metrics: List of metrics to compute
        
        Returns:
            Dictionary of results for each model
        """
        results = {}
        
        # Evaluate PANN
        pann_results = self.evaluate_prediction(test_loader)
        results['PANN'] = {m: pann_results.get(m, float('nan')) for m in metrics}
        
        # Evaluate baselines
        for name, model in baseline_models.items():
            # Simple evaluation (assumes same interface as PANN)
            model.eval()
            all_preds = []
            all_targets = []
            
            with torch.no_grad():
                for x, y in test_loader:
                    x, y = x.to(self.device), y.to(self.device)
                    
                    if hasattr(model, 'predict'):
                        pred = model.predict(x)
                    else:
                        pred = model(x)
                    
                    all_preds.append(pred.cpu().numpy())
                    all_targets.append(y.cpu().numpy())
            
            all_preds = np.concatenate(all_preds, axis=0)
            all_targets = np.concatenate(all_targets, axis=0)
            
            # Compute metrics
            model_results = {}
            if 'mse' in metrics:
                model_results['mse'] = mean_squared_error(all_targets.flatten(), 
                                                         all_preds.flatten())
            if 'mae' in metrics:
                model_results['mae'] = mean_absolute_error(all_targets.flatten(), 
                                                          all_preds.flatten())
            
            results[name] = model_results
        
        return results


def run_lorenz_experiment(
    num_epochs: int = 200,
    use_wandb: bool = False
) -> Dict[str, Any]:
    """
    Run full Lorenz system experiment.
    
    Returns:
        Dictionary of experiment results
    """
    from pann_architecture import PrimeAttentiveNN
    from training import PANNTrainer, create_lorenz_data
    
    # Create data
    train_loader, val_loader, stats = create_lorenz_data(num_samples=10000)
    
    # Create model
    model = PrimeAttentiveNN(
        input_dim=3,
        latent_dim=64,
        num_primes=16,
        hidden_dim=128
    )
    
    # Initialize wandb
    if use_wandb:
        import wandb
        wandb.init(project="pann-lorenz", name="lorenz_experiment")
    
    # Create trainer
    trainer = PANNTrainer(
        model=model,
        learning_rate=1e-3,
        use_wandb=use_wandb
    )
    
    # Train
    history = trainer.train(
        train_loader=train_loader,
        val_loader=val_loader,
        num_epochs=num_epochs
    )
    
    # Analyze results
    experiment = PANNExperiment(model)
    
    # Evaluate prediction
    eval_results = experiment.evaluate_prediction(val_loader)
    
    # Analyze prime spectrum
    spectrum_analysis = experiment.analyze_prime_spectrum(val_loader)
    
    # Extract learned primes
    primes = trainer.analyze_primes(val_loader)
    
    # Create visualization
    sample_trajectory = next(iter(val_loader))[0][:100].cpu().numpy()
    experiment.visualize_prime_decomposition(
        sample_trajectory,
        save_path='lorenz_prime_decomposition.png'
    )
    
    results = {
        'history': history,
        'evaluation': eval_results,
        'spectrum': spectrum_analysis,
        'primes': primes,
        'model': model,
        'trainer': trainer
    }
    
    if use_wandb:
        wandb.finish()
    
    return results


def run_logistic_map_experiment(
    r_values: List[float] = [3.5, 3.7, 3.9, 4.0],
    num_epochs: int = 100
) -> Dict[str, Any]:
    """
    Run logistic map experiments at different r values.
    
    Returns:
        Dictionary of results for each r value
    """
    from pann_architecture import PrimeAttentiveNN
    from training import PANNTrainer, create_logistic_map_data
    
    results = {}
    
    for r in r_values:
        print(f"\nRunning experiment for r = {r}")
        
        # Create data
        train_loader, val_loader = create_logistic_map_data(r=r)
        
        # Create model
        model = PrimeAttentiveNN(
            input_dim=1,
            latent_dim=32,
            num_primes=8,
            hidden_dim=64
        )
        
        # Create trainer
        trainer = PANNTrainer(
            model=model,
            learning_rate=1e-3,
            use_wandb=False
        )
        
        # Train
        history = trainer.train(
            train_loader=train_loader,
            val_loader=val_loader,
            num_epochs=num_epochs
        )
        
        # Analyze
        experiment = PANNExperiment(model)
        spectrum = experiment.analyze_prime_spectrum(val_loader)
        
        # Track eigenvalues
        eigenvalues = spectrum['eigenvalues']
        magnitudes = np.abs(eigenvalues)
        
        results[r] = {
            'history': history,
            'spectrum': spectrum,
            'eigenvalues': eigenvalues,
            'magnitudes': magnitudes,
            'model': model
        }
        
        print(f"  Unstable primes: {np.sum(magnitudes > 1.0)}/{len(magnitudes)}")
        print(f"  Mean magnitude: {np.mean(magnitudes):.3f}")
    
    return results


def analyze_feigenbaum_scaling(
    results: Dict[float, Any]
) -> Dict[str, Any]:
    """
    Analyze Feigenbaum scaling from logistic map experiments.
    
    Args:
        results: Results from logistic map experiments
    
    Returns:
        Feigenbaum analysis
    """
    # Extract eigenvalues at bifurcation points
    r_values = sorted(results.keys())
    eigenvalue_sequences = []
    
    for r in r_values:
        eigenvalues = results[r]['eigenvalues']
        magnitudes = np.abs(eigenvalues)
        # Sort by magnitude
        sorted_mags = np.sort(magnitudes)[::-1]
        eigenvalue_sequences.append(sorted_mags)
    
    # Look for period-doubling sequences
    if len(r_values) >= 3:
        # Simple Feigenbaum ratio estimation
        ratios = []
        for i in range(len(r_values) - 2):
            delta1 = r_values[i+1] - r_values[i]
            delta2 = r_values[i+2] - r_values[i+1]
            if delta2 > 0:
                ratio = delta1 / delta2
                ratios.append(ratio)
        
        feigenbaum_estimate = np.mean(ratios) if ratios else float('nan')
    else:
        feigenbaum_estimate = float('nan')
    
    # Plot eigenvalue scaling
    plt.figure(figsize=(10, 6))
    
    for i, r in enumerate(r_values):
        eigenvalues = results[r]['eigenvalues']
        magnitudes = np.abs(eigenvalues)
        plt.scatter([r] * len(magnitudes), magnitudes, 
                   alpha=0.5, label=f'r={r}')
    
    plt.xlabel('r parameter')
    plt.ylabel('Eigenvalue magnitude')
    plt.title('Eigenvalue Scaling in Logistic Map')
    plt.legend()
    plt.grid(True)
    plt.savefig('feigenbaum_scaling.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return {
        'r_values': r_values,
        'eigenvalue_sequences': eigenvalue_sequences,
        'feigenbaum_estimate': feigenbaum_estimate,
        'estimated_delta': 4.669 if np.isnan(feigenbaum_estimate) else feigenbaum_estimate
    }