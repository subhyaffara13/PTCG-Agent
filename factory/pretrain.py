"""
factory/pretrain.py

Supervised offline pre-training loop via Behavioral Cloning.
"""

import sys
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

logger = logging.getLogger(__name__)


class PreTrainer:
    """Pre-trains a PolicyNetwork using offline expert game files."""
    def __init__(self, state_dim: int = 71, action_dim: int = 3000, model_path: str = 'models/policy_net.pt'):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.model_path = model_path
        
        if TORCH_AVAILABLE:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model = PolicyNetwork(state_dim, 256, action_dim).to(self.device)
            logger.info(f"Initialized PreTrainer on {self.device}")
        else:
            self.model = None

    def train(self, states, actions, epochs: int = 10, batch_size: int = 64, lr: float = 0.001):
        if not TORCH_AVAILABLE:
            logger.error("Cannot train without PyTorch installed.")
            return

        if not states:
            logger.error("No training data provided.")
            return

        dataset = ReplayDataset(states, actions)
        train_size = int(0.8 * len(dataset))
        val_size = len(dataset) - train_size
        train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])
        
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
        
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=lr)
        best_val_loss = float('inf')
        
        for epoch in range(epochs):
            start_time = time.time()
            self.model.train()
            total_loss = 0.0
            
            for batch_states, batch_actions in train_loader:
                batch_states, batch_actions = batch_states.to(self.device), batch_actions.to(self.device)
                optimizer.zero_grad()
                loss = criterion(self.model(batch_states), batch_actions)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
                
            val_loss, val_acc = self.evaluate_loader(val_loader, criterion)
            epoch_time = time.time() - start_time
            logger.info(f"Epoch {epoch+1}/{epochs} | Time: {epoch_time:.1f}s | Train Loss: {total_loss/len(train_loader):.4f} | Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}%")
            
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                os.makedirs('models', exist_ok=True)
                torch.save(self.model.state_dict(), self.model_path)
                logger.info(f"  -> Saved new best model to {self.model_path}")

    def evaluate_loader(self, loader, criterion) -> Tuple[float, float]:
        self.model.eval()
        total_loss, correct, total = 0.0, 0, 0
        with torch.no_grad():
            for states, actions in loader:
                states, actions = states.to(self.device), actions.to(self.device)
                outputs = self.model(states)
                total_loss += criterion(outputs, actions).item()
                _, predicted = torch.max(outputs.data, 1)
                total += actions.size(0)
                correct += (predicted == actions).sum().item()
        return total_loss / len(loader), 100 * correct / total

    def evaluate(self, states, actions, batch_size: int = 64) -> dict:
        if not TORCH_AVAILABLE:
            return {"loss": 0.0, "accuracy": 0.0}
        dataset = ReplayDataset(states, actions)
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
        loss, acc = self.evaluate_loader(loader, nn.CrossEntropyLoss())
        return {"loss": loss, "accuracy": acc}


if __name__ == '__main__':
    import argparse
    from factory.data_alignment import DataAligner
    
    parser = argparse.ArgumentParser(description="Offline Pre-training via Behavioral Cloning")
    parser.add_argument('--data_dir', type=str, default='data/expert_replays')
    parser.add_argument('--epochs', type=int, default=10)
    parser.add_argument('--batch_size', type=int, default=64)
    args = parser.parse_args()
    
    aligner = DataAligner()
    states, actions = aligner.build_training_dataset([])
    
    if not states:
        import random
        states = [[random.random() for _ in range(71)] for _ in range(1000)]
        actions = [random.randint(0, 100) for _ in range(1000)]
        
    trainer = PreTrainer()
    trainer.train(states, actions, epochs=args.epochs, batch_size=args.batch_size)
