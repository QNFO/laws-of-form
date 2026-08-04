"""
Main script for running Prime-Attentive Neural Network experiments.
"""
import argparse
import torch
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import json
import warnings
warnings.filterwarnings('ignore')

# Import local modules
from pann_architecture import PrimeAttentiveNN
from training import PANNTrainer, create_lorenz_data, create_logistic_map_data
from experiments import (PANNExperiment, run_lorenz_experiment, 
                        run_logistic_map_experiment, analyze_feigenbaum_scaling)
from topological_regularization import TopologyAwareLoss, analyze_topological_invariants


def parse_args():
    parser = argparse.ArgumentParser(description='Prime-Attentive Neural Networks for Chaos')
    
    # Experiment type
    parser.add_argument('--experiment', type=str, default='lorenz',
                       choices=['lorenz', 'logistic', 'rossler', 'custom'],
                       help='Which experiment to run')
    
    # Model parameters
    parser.add_argument('--input_dim', type=int, default=3,
                       help='Input dimension')
    parser.add_argument('--latent_dim', type=int, default=64,
                       help='Latent dimension')
    parser.add_argument('--num_primes', type=int, default=16,
                       help='Number of primes')
    parser.add_argument('--hidden_dim', type=int, default=128,
                       help='Hidden dimension')
    
    # Training parameters
    parser.add_argument('--num_epochs', type=int, default=200,
                       help='Number of training epochs')
    parser.add_argument('--batch_size', type=int, default=32,
                       help='Batch size')
    parser.add_argument('--learning_rate', type=float, default=1e-3,
                       help='Learning rate')
    parser.add_argument('--topology_weight', type=float, default=0.1,
                       help='Weight for topological regularization')
    
    # Data parameters
    parser.add_argument('--num_samples', type=int, default=10000,
                       help='Number of data samples')
    parser.add_argument('--dt', type=float, default=0.01,
                       help='Time step for data generation')
    
    # Logistic map parameters
    parser.add_argument('--r_values', type=float, nargs='+',
                       default=[3.5, 3.7, 3.9, 4.0],
                       help='r values for logistic map experiments')
    
    # Output parameters
    parser.add_argument('--output_dir', type=str, default='results',
                       help='Output directory for results')
    parser.add_argument('--save_model', action='store_true',
                       help='Save trained model')
    parser.add_argument('--visualize', action='store_true',
                       help='Generate visualizations')
    parser.add_argument('--use_wandb', action='store_true',
                       help='Use Weights & Biases for logging')
    
    return parser.parse_args()


def setup_environment(args):
    """Setup environment and create output directory."""
    # Set random seeds
    torch.manual_seed(42)
    np.random.seed(42)
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Save configuration
    config_path = output_dir / 'config.json'
    with open(config_path, 'w') as f:
        json.dump(vars(args), f, indent=2)
    
    print(f"Configuration saved to {config_path}")
    return output_dir


def run_lorenz_experiment_wrapper(args, output_dir):
    """Wrapper for Lorenz experiment."""
    print("\n" + "="*60)
    print("Running Lorenz System Experiment")
    print("="*60)
    
    results = run_lorenz_experiment(
        num_epochs=args.num_epochs,
        use_wandb=args.use_wandb
    )
    
    # Save results
    results_path = output_dir / 'lorenz_results.pth'
    torch.save(results, results_path)
    print(f"Results saved to {results_path}")
    
    # Generate report
    generate_report(results, output_dir / 'lorenz_report.txt')
    
    return results


def run_logistic_experiment_wrapper(args, output_dir):
    """Wrapper for logistic map experiments."""
    print("\n" + "="*60)
    print("Running Logistic Map Experiments")
    print("="*60)
    
    results = run_logistic_map_experiment(
        r_values=args.r_values,
        num_epochs=args.num_epochs // 2  # Logistic map trains faster
    )
    
    # Analyze Feigenbaum scaling
    feigenbaum_analysis = analyze_feigenbaum_scaling(results)
    
    # Save results
    results_path = output_dir / 'logistic_results.pth'
    torch.save({'results': results, 'feigenbaum': feigenbaum_analysis}, results_path)
    print(f"Results saved to {results_path}")
    
    # Generate report
    generate_report({'results': results, 'feigenbaum': feigenbaum_analysis}, 
                   output_dir / 'logistic_report.txt')
    
    return results


def generate_report(results, filepath):
    """Generate a text report of experiment results."""
    with open(filepath, 'w') as f:
        f.write("Prime-Attentive Neural Network Experiment Report\n")
        f.write("="*50 + "\n\n")
        
        if 'evaluation' in results:
            # Lorenz results
            f.write("Lorenz System Results:\n")
            f.write("-"*30 + "\n")
            
            eval_results = results['evaluation']
            f.write(f"Prediction MSE: {eval_results['mse']:.6f}\n")
            f.write(f"Prediction MAE: {eval_results['mae']:.6f}\n")
            f.write(f"Estimated Lyapunov Time: {eval_results.get('lyapunov_time', 'N/A')}\n")
            
            if 'spectrum' in results:
                spectrum = results['spectrum']
                f.write(f"\nPrime Spectrum Analysis:\n")
                f.write(f"Number of unstable primes: {spectrum['num_unstable']}\n")
                f.write(f"Number of oscillatory primes: {spectrum['num_oscillatory']}\n")
                f.write(f"Spectral entropy: {spectrum['spectral_entropy']:.3f}\n")
        
        elif 'feigenbaum' in results:
            # Logistic map results
            f.write("Logistic Map Results:\n")
            f.write("-"*30 + "\n")
            
            feigenbaum = results['feigenbaum']
            f.write(f"Estimated Feigenbaum constant: {feigenbaum['feigenbaum_estimate']:.3f}\n")
            f.write(f"Theoretical value (δ): 4.669201609...\n")
            
            if 'results' in results:
                logistic_results = results['results']
                for r, res in logistic_results.items():
                    f.write(f"\nr = {r}:\n")
                    spectrum = res['spectrum']
                    f.write(f"  Unstable primes: {spectrum['num_unstable']}/{len(spectrum['eigenvalues'])}\n")
                    f.write(f"  Max eigenvalue magnitude: {np.max(spectrum['magnitudes']):.3f}\n")
        
        f.write("\n" + "="*50 + "\n")
        f.write("Experiment completed successfully.\n")


def visualize_results(results, output_dir):
    """Generate visualizations of results."""
    print("\nGenerating visualizations...")
    
    if 'evaluation' in results:
        # Lorenz visualizations
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Training history
        if 'history' in results:
            history = results['history']
            ax = axes[0, 0]
            ax.plot(history['train_loss'], label='Train Loss')
            ax.plot(history['val_loss'], label='Val Loss')
            ax.set_xlabel('Epoch')
            ax.set_ylabel('Loss')
            ax.set_title('Training History')
            ax.legend()
            ax.grid(True)
        
        # Prime importance
        if 'primes' in results:
            primes = results['primes']
            importance = [p['importance'] for p in primes]
            lyapunov_exps = [p['lyapunov_exponent'] for p in primes]
            
            ax = axes[0, 1]
            bars = ax.bar(range(len(importance)), importance)
            ax.set_xlabel('Prime Index')
            ax.set_ylabel('Importance')
            ax.set_title('Prime Importance')
            
            # Color by Lyapunov exponent
            for bar, exp in zip(bars, lyapunov_exps):
                bar.set_color('red' if exp > 0 else 'blue')
        
        # Eigenvalue spectrum
        if 'spectrum' in results:
            spectrum = results['spectrum']
            eigenvalues = spectrum['eigenvalues']
            
            ax = axes[1, 0]
            scatter = ax.scatter(eigenvalues.real, eigenvalues.imag, 
                                c=np.arange(len(eigenvalues)), cmap='viridis')
            ax.axhline(y=0, color='k', linestyle='--', alpha=0.3)
            ax.axvline(x=1.0, color='k', linestyle='--', alpha=0.3)
            ax.set_xlabel('Real(λ)')
            ax.set_ylabel('Imag(λ)')
            ax.set_title('Eigenvalue Spectrum')
            ax.grid(True)
            plt.colorbar(scatter, ax=ax, label='Prime Index')
        
        # Prediction example
        if 'evaluation' in results:
            eval_results = results['evaluation']
            if 'predictions' in eval_results and 'targets' in eval_results:
                ax = axes[1, 1]
                predictions = eval_results['predictions']
                targets = eval_results['targets']
                
                time_steps = min(100, len(predictions))
                ax.plot(targets[:time_steps, 0], label='True')
                ax.plot(predictions[:time_steps, 0, 0], label='Predicted', alpha=0.7)
                ax.set_xlabel('Time Step')
                ax.set_ylabel('State')
                ax.set_title('Prediction Example (x-component)')
                ax.legend()
                ax.grid(True)
        
        plt.tight_layout()
        plt.savefig(output_dir / 'lorenz_summary.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    print(f"Visualizations saved to {output_dir}")


def main():
    args = parse_args()
    output_dir = setup_environment(args)
    
    # Run experiment based on type
    if args.experiment == 'lorenz':
        results = run_lorenz_experiment_wrapper(args, output_dir)
    elif args.experiment == 'logistic':
        results = run_logistic_experiment_wrapper(args, output_dir)
    else:
        raise ValueError(f"Unknown experiment type: {args.experiment}")
    
    # Generate visualizations if requested
    if args.visualize:
        visualize_results(results, output_dir)
    
    # Save model if requested
    if args.save_model and 'model' in results:
        model_path = output_dir / 'trained_model.pth'
        torch.save(results['model'].state_dict(), model_path)
        print(f"Model saved to {model_path}")
    
    print("\n" + "="*60)
    print("Experiment completed successfully!")
    print(f"Results saved to: {output_dir}")
    print("="*60)


if __name__ == "__main__":
    main()