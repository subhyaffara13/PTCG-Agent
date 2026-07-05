"""
agents/value_network_helpers.py
Defines the PyTorch MLP Value Network architecture for CPU-only training/evals.
"""
import os
is_kaggle = any(k.startswith("KAGGLE") for k in os.environ)

if is_kaggle:
    # On Kaggle, skip torch entirely to avoid environment crashes
    PTCGValueMLP = None
    state_to_tensor = None
else:
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
            
            my_bench = game_state.get("my_bench", [])
            opp_bench = game_state.get("opponent_bench", [])
            my_bench_size = len(my_bench) if isinstance(my_bench, list) else 0
            opp_bench_size = len(opp_bench) if isinstance(opp_bench, list) else 0
            
            my_hand = game_state.get("my_hand", [])
            my_hand_size = len(my_hand) if isinstance(my_hand, list) else 0
            
            turn = game_state.get("turn_number", 0)
            
            my_discard = game_state.get("my_discard_pile", [])
            opp_discard = game_state.get("opponent_discard_pile", [])
            my_discard_size = len(my_discard) if isinstance(my_discard, list) else 0
            opp_discard_size = len(opp_discard) if isinstance(opp_discard, list) else 0
            
            stadium = 1.0 if game_state.get("stadium_card") else 0.0
            
            weakness_mult = 0.0
            resistance_mult = 0.0
            
            opp_active = game_state.get("opponent_active_pokemon", {}) or {}
            if isinstance(active, dict) and isinstance(opp_active, dict):
                my_type = active.get("element_type", "")
                opp_weakness = opp_active.get("weakness", "")
                opp_resistance = opp_active.get("resistance", "")
                if my_type and opp_weakness and my_type.lower() == opp_weakness.lower():
                    weakness_mult = 1.0
                if my_type and opp_resistance and my_type.lower() == opp_resistance.lower():
                    resistance_mult = 1.0
            
            # 14 extracted features + padding to 20
            features = [
                float(my_prizes) / 6.0, 
                float(opp_prizes) / 6.0, 
                float(my_active_hp), 
                float(opp_active_hp), 
                float(attached) / 10.0,
                float(my_bench_size) / 5.0,
                float(opp_bench_size) / 5.0,
                float(my_hand_size) / 10.0,
                float(turn) / 20.0,
                float(my_discard_size) / 60.0,
                float(opp_discard_size) / 60.0,
                stadium,
                weakness_mult,
                resistance_mult
            ] + [0.0]*6
            
            return torch.tensor(features, dtype=torch.float32).unsqueeze(0)
    except ImportError:
        PTCGValueMLP = None
        state_to_tensor = None
