"""
Training utilities for Prime-Attentive Neural Networks.
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
import wandb
from tqdm import tqdm
import os


class PANNTrainer:
    """
    Trainer for Prime-Attentive Neural Networks.
    """
    
    def __init__(
        self,
        model: nn.Module,
        device: str = None,
        learning_rate: float = 1e-3,
        weight_decay: float = 1e-5,
        use_wandb: bool = False
    ):
        if device is None:
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        self.model = model.to(device)
        self.device = device
        self.use_wandb = use_wandb
        
        # Optimizer
        self.optimizer = optim.AdamW(
            model.parameters(),
            lr=learning_rate,
            weight_decay=weight_decay
        )
        
        # Learning rate scheduler
        self.scheduler = optim.lr_scheduler.CosineAnnealingLR(
            self.optimizer,
            T_max=100,
            eta_min=1e-6
        )
        
        # Loss function
        self.criterion = nn.MSELoss()
        
        # Tracking
        self.train_losses = []
        self.val_losses = []
        self.best_val_loss = float('inf')
        
    def train_epoch(
        self,
        train_loader: DataLoader,
        epoch: int,
        topology_loss_weight: float = 0.1
    ) -> Dict[str, float]:
        """
        Train for one epoch.
        
        Args:
            train_loader: Training data loader
            epoch: Current epoch number
            topology_loss_weight: Weight for topological regularization
        
        Returns:
            Dictionary of training metrics
        """
        self.model.train()
        total_loss = 0.0
        total_pred_loss = 0.0
        total_reg_loss = 0.0
        
        pbar = tqdm(train_loader, desc=f"Epoch {epoch}")
        for batch_idx, (x, y) in enumerate(pbar):
            x, y = x.to(self.device), y.to(self.device)
            
            # Forward pass
            outputs = self.model(x, dt=0.01)
            
            # Compute prediction loss
            pred_loss = self.criterion(outputs['x_pred'], y)
            
            # Combine with regularization losses
            reg_loss = outputs.get('reg_loss', torch.tensor(0.0))
            loss = pred_loss + topology_loss_weight * reg_loss
            
            # Backward pass
            self.optimizer.zero_grad()
            loss.backward()
            
            # Gradient clipping
            torch.nn.utils.clip_grad_norm_(
                self.model.parameters(),
                max_norm=1.0
            )
            
            self.optimizer.step()
            
            # Track metrics
            total_loss += loss.item()
            total_pred_loss += pred_loss.item()
            total_reg_loss += reg_loss.item()
            
            # Update progress bar
            pbar.set_postfix({
                'loss': loss.item(),
                'pred': pred_loss.item(),
                'reg': reg_loss.item()
            })
        
        # Average metrics
        avg_loss = total_loss / len(train_loader)
        avg_pred_loss = total_pred_loss / len(train_loader)
        avg_reg_loss = total_reg_loss / len(train_loader)
        
        metrics = {
            'train_loss': avg_loss,
            'train_pred_loss': avg_pred_loss,
            'train_reg_loss': avg_reg_loss
        }
        
        # Log to wandb
        if self.use_wandb:
            wandb.log(metrics)
        
        self.train_losses.append(avg_loss)
        return metrics
    
    def validate(
        self,
        val_loader: DataLoader,
        epoch: int
    ) -> Dict[str, float]:
        """
        Validate the model.
        
        Args:
            val_loader: Validation data loader
            epoch: Current epoch number
        
        Returns:
            Dictionary of validation metrics
        """
        self.model.eval()
        total_loss = 0.0
        total_pred_loss = 0.0
        
        with torch.no_grad():
            for x, y in val_loader:
                x, y = x.to(self.device), y.to(self.device)
                
                # Forward pass
                outputs = self.model(x, dt=0.01)
                
                # Compute losses
                pred_loss = self.criterion(outputs['x_pred'], y)
                reg_loss = outputs.get('reg_loss', torch.tensor(0.0))
                loss = pred_loss + 0.1 * reg_loss
                
                total_loss += loss.item()
                total_pred_loss += pred_loss.item()
        
        # Average metrics
        avg_loss = total_loss / len(val_loader)
        avg_pred_loss = total_pred_loss / len(val_loader)
        
        metrics = {
            'val_loss': avg_loss,
            'val_pred_loss': avg_pred_loss
        }
        
        # Update best model
        if avg_loss < self.best_val_loss:
            self.best_val_loss = avg_loss
            self.save_checkpoint('best_model.pth')
        
        # Log to wandb
        if self.use_wandb:
            wandb.log(metrics)
        
        self.val_losses.append(avg_loss)
        return metrics
    
    def train(
        self,
        train_loader: DataLoader,
        val_loader: DataLoader,
        num_epochs: int = 100,
        save_dir: str = 'checkpoints',
        topology_loss_weight: float = 0.1
    ) -> Dict[str, List[float]]:
        """
        Complete training loop.
        
        Args:
            train_loader: Training data loader
            val_loader: Validation data loader
            num_epochs: Number of training epochs
            save_dir: Directory to save checkpoints
            topology_loss_weight: Weight for topological regularization
        
        Returns:
            Training history
        """
        os.makedirs(save_dir, exist_ok=True)
        
        history = {
            'train_loss': [],
            'val_loss': [],
            'train_pred_loss': [],
            'val_pred_loss': []
        }
        
        for epoch in range(num_epochs):
            # Train
            train_metrics = self.train_epoch(
                train_loader, epoch, topology_loss_weight
            )
            
            # Validate
            val_metrics = self.validate(val_loader, epoch)
            
            # Update learning rate
            self.scheduler.step()
            
            # Save checkpoint
            if epoch % 10 == 0:
                self.save_checkpoint(
                    os.path.join(save_dir, f'checkpoint_epoch_{epoch}.pth')
                )
            
            # Update history
            history['train_loss'].append(train_metrics['train_loss'])
            history['val_loss'].append(val_metrics['val_loss'])
            history['train_pred_loss'].append(train_metrics['train_pred_loss'])
            history['val_pred_loss'].append(val_metrics['val_pred_loss'])
            
            # Print progress
            print(f"\nEpoch {epoch}:")
            print(f"  Train Loss: {train_metrics['train_loss']:.6f}")
            print(f"  Val Loss: {val_metrics['val_loss']:.6f}")
            print(f"  LR: {self.scheduler.get_last_lr()[0]:.6f}")
        
        return history
    
    def save_checkpoint(self, path: str):
        """Save model checkpoint."""
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
            'train_losses': self.train_losses,
            'val_losses': self.val_losses,
            'best_val_loss': self.best_val_loss
        }, path)
    
    def load_checkpoint(self, path: str):
        """Load model checkpoint."""
        checkpoint = torch.load(path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        self.train_losses = checkpoint['train_losses']
        self.val_losses = checkpoint['val_losses']
        self.best_val_loss = checkpoint['best_val_loss']
    
    def analyze_primes(self, data_loader: DataLoader) -> List[Dict[str, Any]]:
        """
        Analyze learned primes on validation data.
        
        Args:
            data_loader: Data loader for analysis
        
        Returns:
            List of prime analyses
        """
        self.model.eval()
        all_coeffs = []
        
        with torch.no_grad():
            for x, _ in data_loader:
                x = x.to(self.device)
                outputs = self.model(x, dt=0.01)
                all_coeffs.append(outputs['coeffs'].cpu().numpy())
        
        # Concatenate all coefficients
        all_coeffs = np.vstack(all_coeffs)
        
        # Analyze each prime
        primes = self.model.extract_primes()
        for i, prime in enumerate(primes):
            # Add activation statistics
            prime['mean_activation'] = np.mean(np.abs(all_coeffs[:, i]))
            prime['activation_std'] = np.std(all_coeffs[:, i])
            prime['activation_sparsity'] = np.mean(all_coeffs[:, i] == 0)
        
        return primes


def create_lorenz_data(
    num_samples: int = 10000,
    dt: float = 0.01,
    sigma: float = 10.0,
    rho: float = 28.0,
    beta: float = 8.0/3.0,
    train_split: float = 0.8
) -> Tuple[DataLoader, DataLoader]:
    """
    Generate Lorenz system data for training.
    
    Returns:
        Tuple of (train_loader, val_loader)
    """
    # Generate trajectory
    x = np.zeros((num_samples, 3))
    x[0] = [1.0, 1.0, 1.0]
    
    for i in range(num_samples - 1):
        dx = sigma * (x[i, 1] - x[i, 0])
        dy = x[i, 0] * (rho - x[i, 2]) - x[i, 1]
        dz = x[i, 0] * x[i, 1] - beta * x[i, 2]
        x[i + 1] = x[i] + dt * np.array([dx, dy, dz])
    
    # Create input-output pairs
    X = x[:-1]
    y = x[1:]
    
    # Normalize
    X_mean, X_std = X.mean(axis=0), X.std(axis=0)
    y_mean, y_std = y.mean(axis=0), y.std(axis=0)
    
    X = (X - X_mean) / X_std
    y = (y - y_mean) / y_std
    
    # Split
    split_idx = int(train_split * len(X))
    X_train, X_val = X[:split_idx], X[split_idx:]
    y_train, y_val = y[:split_idx], y[split_idx:]
    
    # Create datasets
    train_dataset = TensorDataset(
        torch.FloatTensor(X_train),
        torch.FloatTensor(y_train)
    )
    val_dataset = TensorDataset(
        torch.FloatTensor(X_val),
        torch.FloatTensor(y_val)
    )
    
    # Create loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=32,
        shuffle=True
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=32,
        shuffle=False
    )
    
    return train_loader, val_loader, (X_mean, X_std, y_mean, y_std)


def create_logistic_map_data(
    r: float = 3.9,
    num_samples: int = 5000,
    train_split: float = 0.8
) -> Tuple[DataLoader, DataLoader]:
    """
    Generate logistic map data for training.
    """
    # Generate trajectory
    x = np.zeros(num_samples)
    x[0] = 0.5
    
    for i in range(num_samples - 1):
        x[i + 1] = r * x[i] * (1 - x[i])
    
    # Create input-output pairs
    X = x[:-1].reshape(-1, 1)
    y = x[1:].reshape(-1, 1)
    
    # Split
    split_idx = int(train_split * len(X))
    X_train, X_val = X[:split_idx], X[split_idx:]
    y_train, y_val = y[:split_idx], y[split_idx:]
    
    # Create datasets
    train_dataset = TensorDataset(
        torch.FloatTensor(X_train),
        torch.FloatTensor(y_train)
    )
    val_dataset = TensorDataset(
        torch.FloatTensor(X_val),
        torch.FloatTensor(y_val)
    )
    
    # Create loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=32,
        shuffle=True
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=32,
        shuffle=False
    )
    
    return train_loader, val_loader