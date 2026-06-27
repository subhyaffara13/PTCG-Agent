"""
factory/pretrain.py
Supervised offline pre-training loop via Behavioral Cloning.
"""
import logging
import time
import os
from typing import Tuple

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader
except ImportError:
    pass

from factory.pretrain_dataset import PolicyNetwork, ReplayDataset, TORCH_AVAILABLE
from factory.pretrain_helpers import run_evaluation_loader, run_train_epoch
from factory.state_dimensions import STATE_DIM

logger = logging.getLogger(__name__)

class PreTrainer:
    def __init__(self, state_dim: int = STATE_DIM, action_dim: int = 3000, model_path: str = 'models/policy_net.pt'):
        self.state_dim, self.action_dim, self.model_path = state_dim, action_dim, model_path
        if TORCH_AVAILABLE:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model = PolicyNetwork(state_dim, 256, action_dim).to(self.device)
            logger.info(f"Initialized PreTrainer on {self.device}")
        else:
            self.model = None

    def train(self, states, actions, epochs: int = 10, batch_size: int = 64, lr: float = 0.001):
        if not TORCH_AVAILABLE or not states:
            logger.error("Cannot train: PyTorch missing or empty states.")
            return

        dataset = ReplayDataset(states, actions)
        train_size = int(0.8 * len(dataset))
        train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, len(dataset) - train_size])
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
        
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=lr)
        best_val_loss = float('inf')
        
        for epoch in range(epochs):
            start_time = time.time()
            total_loss = run_train_epoch(self.model, train_loader, self.device, optimizer, criterion)
            val_loss, val_acc = self.evaluate_loader(val_loader, criterion)
            logger.info(f"Epoch {epoch+1}/{epochs} | Time: {time.time() - start_time:.1f}s | Train Loss: {total_loss/len(train_loader):.4f} | Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}%")
            
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                os.makedirs('models', exist_ok=True)
                torch.save(self.model.state_dict(), self.model_path)
                logger.info(f"  -> Saved new best model to {self.model_path}")

    def evaluate_loader(self, loader, criterion) -> Tuple[float, float]:
        return run_evaluation_loader(self.model, loader, self.device, criterion)

    def evaluate(self, states, actions, batch_size: int = 64) -> dict:
        if not TORCH_AVAILABLE: return {"loss": 0.0, "accuracy": 0.0}
        dataset = ReplayDataset(states, actions)
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
        loss, acc = self.evaluate_loader(loader, nn.CrossEntropyLoss())
        return {"loss": loss, "accuracy": acc}
