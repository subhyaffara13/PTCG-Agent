"""
agents/value_network_helpers.py
Defines the PyTorch MLP Value Network architecture for CPU-only training/evals.
"""
try:
    import torch
    import torch.nn as nn
    
    class PTCGValueMLP(nn.Module):
        def __init__(self, input_dim=20):
            super().__init__()
            self.model = nn.Sequential(
                nn.Linear(input_dim, 64),
                nn.ReLU(),
                nn.Linear(64, 32),
                nn.ReLU(),
                nn.Linear(32, 1),
                nn.Tanh()
            )
            
        def forward(self, x):
            return self.model(x)
            
    def state_to_tensor(game_state: dict) -> torch.Tensor:
        """Converts game state dictionary to a numeric tensor for the MLP."""
        my_prizes = game_state.get("my_prizes", 6)
        opp_prizes = game_state.get("opponent_prizes", 6)
        my_active_hp = game_state.get("my_active_hp", 100) / 100.0
        opp_active_hp = game_state.get("opponent_active_hp", 100) / 100.0
        
        active = game_state.get("my_active_pokemon", {}) or {}
        attached = len(active.get("attached", []) or active.get("energies", [])) if isinstance(active, dict) else 0
        
        features = [
            float(my_prizes), float(opp_prizes), float(my_active_hp), float(opp_active_hp), float(attached),
        ] + [0.0]*15
        
        return torch.tensor(features, dtype=torch.float32).unsqueeze(0)
except ImportError:
    PTCGValueMLP = None
    state_to_tensor = None
