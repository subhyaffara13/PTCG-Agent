import random
import logging
from cb_agents.value_network import BaseValueNetwork
from cb_agents.card_registry import CardRegistry
from cb_agents.heuristic_pipeline import _state_heuristics, _action_score

logger = logging.getLogger(__name__)

class HeuristicValueNetwork(BaseValueNetwork):
    def __init__(self):
        self._nn_model = None
        try:
            import os, torch
            model_path = "models/ppo_actor_critic.pt"
            if not os.path.exists(model_path):
                model_path = "logs/model_weights.pth"
            if os.path.exists(model_path):
                from factory.state_dimensions import STATE_DIM
                from factory.ppo_trainer_network import ActorCritic
                dev = torch.device("cpu")
                model = ActorCritic(STATE_DIM, 256, 3000)
                if hasattr(model, "to"):
                    model = model.to(dev)
                if hasattr(model, "load_state_dict"):
                    model.load_state_dict(torch.load(model_path, map_location=dev, weights_only=True))
                if hasattr(model, "eval"):
                    model.eval()
                self._nn_model = model
        except Exception:
            pass

    def evaluate(self, game_state: dict, action: str | None = None, determinization: dict | None = None) -> float:
        if action is None:
            return 0.0
        if game_state.get("game_over"):
            return 1.0 if game_state.get("winner") == "me" else -1.0
        value = _state_heuristics(game_state)
        threat_penalty = 0.0
        if determinization and determinization.get("hand"):
            threat_penalty = len(determinization["hand"]) * 0.01
        value += _action_score(action, game_state, threat_penalty)
        value += random.uniform(-0.01, 0.01)
        h_val = max(-1.0, min(1.0, value))
        
        if self._nn_model is not None:
            try:
                import torch
                from factory.state_dimensions import encode_state_vector
                vec = torch.tensor(encode_state_vector(game_state), dtype=torch.float32).unsqueeze(0)
                with torch.no_grad():
                    _, nn_v = self._nn_model(vec)
                    nn_val = float(torch.tanh(nn_v).item())
                    # Calibrated hybrid blend: 40% NN + 60% Heuristic
                    return max(-1.0, min(1.0, 0.4 * nn_val + 0.6 * h_val))
            except Exception:
                pass
                
        return h_val
