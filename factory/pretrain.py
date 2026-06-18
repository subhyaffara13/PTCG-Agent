import sys
import logging
import time
from typing import Tuple

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import Dataset, DataLoader
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("PyTorch not available. PreTrainer will use a mock implementation.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if TORCH_AVAILABLE:
    class PolicyNetwork(nn.Module):
        def __init__(self, input_dim: int, hidden_dim: int, output_dim: int):
            super().__init__()
            self.network = nn.Sequential(
                nn.Linear(input_dim, hidden_dim),
                nn.ReLU(),
                nn.LayerNorm(hidden_dim),
                nn.Linear(hidden_dim, hidden_dim // 2),
                nn.ReLU(),
                nn.LayerNorm(hidden_dim // 2),
                nn.Linear(hidden_dim // 2, output_dim)
            )
            
        def forward(self, x):
            return self.network(x)

    class ReplayDataset(Dataset):
        def __init__(self, states, actions):
            self.states = torch.FloatTensor(states)
            self.actions = torch.LongTensor(actions)
            
        def __len__(self):
            return len(self.states)
            
        def __getitem__(self, idx):
            return self.states[idx], self.actions[idx]

class PreTrainer:
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
        """Supervised training loop over offline data."""
        if not TORCH_AVAILABLE:
            logger.error("Cannot train without PyTorch installed.")
            return

        if len(states) == 0:
            logger.error("No training data provided.")
            return

        dataset = ReplayDataset(states, actions)
        # Split into train/val
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
                batch_states = batch_states.to(self.device)
                batch_actions = batch_actions.to(self.device)
                
                optimizer.zero_grad()
                outputs = self.model(batch_states)
                loss = criterion(outputs, batch_actions)
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
                
            avg_train_loss = total_loss / len(train_loader)
            
            # Validation
            val_loss, val_acc = self.evaluate_loader(val_loader, criterion)
            
            epoch_time = time.time() - start_time
            logger.info(f"Epoch {epoch+1}/{epochs} | Time: {epoch_time:.1f}s | Train Loss: {avg_train_loss:.4f} | Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}%")
            
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                import os
                os.makedirs('models', exist_ok=True)
                torch.save(self.model.state_dict(), self.model_path)
                logger.info(f"  -> Saved new best model to {self.model_path}")

    def evaluate_loader(self, loader, criterion) -> Tuple[float, float]:
        """Evaluate model on a dataloader."""
        self.model.eval()
        total_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for states, actions in loader:
                states = states.to(self.device)
                actions = actions.to(self.device)
                
                outputs = self.model(states)
                loss = criterion(outputs, actions)
                total_loss += loss.item()
                
                _, predicted = torch.max(outputs.data, 1)
                total += actions.size(0)
                correct += (predicted == actions).sum().item()
                
        avg_loss = total_loss / len(loader)
        accuracy = 100 * correct / total
        return avg_loss, accuracy

    def evaluate(self, states, actions, batch_size: int = 64) -> dict:
        """Compute accuracy on held-out data lists."""
        if not TORCH_AVAILABLE:
            return {"loss": 0.0, "accuracy": 0.0}
            
        dataset = ReplayDataset(states, actions)
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
        criterion = nn.CrossEntropyLoss()
        
        loss, acc = self.evaluate_loader(loader, criterion)
        return {"loss": loss, "accuracy": acc}

if __name__ == '__main__':
    # CLI entry point for offline training
    import argparse
    from factory.data_alignment import DataAligner
    
    parser = argparse.ArgumentParser(description="Offline Pre-training via Behavioral Cloning")
    parser.add_argument('--data_dir', type=str, default='data/expert_replays', help='Directory containing JSON/CSV replays')
    parser.add_argument('--epochs', type=int, default=10, help='Number of training epochs')
    parser.add_argument('--batch_size', type=int, default=64, help='Batch size')
    args = parser.parse_args()
    
    logger.info(f"Starting PreTrainer with data from {args.data_dir}")
    
    aligner = DataAligner()
    # In a real scenario we would glob files from data_dir
    dummy_files = [] 
    
    states, actions = aligner.build_training_dataset(dummy_files)
    
    if len(states) == 0:
        logger.warning("No data found for pretraining. Generating synthetic data for testing.")
        import random
        # Generate dummy data for testing the loop
        states = [[random.random() for _ in range(71)] for _ in range(1000)]
        actions = [random.randint(0, 100) for _ in range(1000)]
        
    trainer = PreTrainer()
    trainer.train(states, actions, epochs=args.epochs, batch_size=args.batch_size)
