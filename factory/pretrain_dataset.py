"""
factory/pretrain_dataset.py

Defines the PolicyNetwork architecture and ReplayDataset for pre-training.
"""

import logging

try:
    import torch
    import torch.nn as nn
    from torch.utils.data import Dataset
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("PyTorch not available. PolicyNetwork and ReplayDataset cannot be defined.")

if TORCH_AVAILABLE:
    class PolicyNetwork(nn.Module):
        """
        Policy network for behavioral cloning supervised pre-training.
        """
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
        """
        Custom PyTorch Dataset wrapping offline state-action trajectories.
        """
        def __init__(self, states, actions):
            self.states = torch.FloatTensor(states)
            self.actions = torch.LongTensor(actions)
            
        def __len__(self):
            return len(self.states)
            
        def __getitem__(self, idx):
            return self.states[idx], self.actions[idx]
else:
    class PolicyNetwork:
        def __init__(self, *args, **kwargs):
            pass
    class ReplayDataset:
        def __init__(self, *args, **kwargs):
            pass
