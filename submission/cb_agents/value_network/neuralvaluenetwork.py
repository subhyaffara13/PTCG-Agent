from . import Any, logger, os, torch
from .__getattr___actionprior_basevaluenetwork import BaseValueNetwork

class NeuralValueNetwork(BaseValueNetwork):
    heuristic: Any
    model: Any
    state_to_tensor: Any
    state_to_card_tokens: Any
    inference_client: Any

    def __init__(self, model_path: str = "logs/model_weights.pth", device: str = "cpu"):
        from cb_agents.value_network_helpers import ActorCritic, state_to_tensor, state_to_card_tokens, HAS_TORCH
        try: from cb_agents.state_dimensions import STATE_DIM
        except ImportError: from factory.state_dimensions import STATE_DIM

        self.device = device
        self.model = None
        self.state_to_tensor = state_to_tensor
        self.state_to_card_tokens = state_to_card_tokens
        self.has_torch = HAS_TORCH

        # Initialize TCP InferenceClient
        try:
            from factory.inference_client import InferenceClient
            host = os.environ.get("MASTER_HOST", "127.0.0.1")
            self.inference_client = InferenceClient(host=host, port=9999)
        except Exception:
            self.inference_client = None

        if HAS_TORCH:
            try:
                import torch
                tnet = ActorCritic(input_dim=STATE_DIM, hidden_dim=256, action_dim=3000)
                tnet.to(self.device)
                
                if os.path.exists(model_path):
                    state_dict = torch.load(model_path, map_location=self.device, weights_only=True)
                    model_keys = set(state_dict.keys())
                    if any("encoder" in k or "actor" in k for k in model_keys):
                        tnet.load_state_dict(state_dict, strict=False)
                        self.model = tnet
                        self.model.eval()
                        logger.info(f"Loaded ActorCritic from {model_path} successfully.")
                    else:
                        logger.warning("Checkpoint keys do not match ActorCritic. Falling back to HeuristicValueNetwork.")
                else:
                    logger.warning(f"No checkpoint found at {model_path}. Using untutored ActorCritic.")
                    self.model = tnet
                    self.model.eval()
            except Exception as e:
                logger.warning(f"ActorCritic load failed: {e}. Falling back to HeuristicValueNetwork.")
                self.model = None

    def evaluate(self, game_state: dict, action: str | None = None, determinization: dict | None = None) -> float:
        if game_state.get("game_over"):
            return 1.0 if game_state.get("winner") == "me" else -1.0

        # Try batched inference server first
        try:
            if hasattr(self, 'inference_client') and self.inference_client and self.inference_client.is_available():
                _, val = self.inference_client.evaluate(game_state)
                if val is not None:
                    if action:
                        from cb_agents.heuristic_pipeline import _action_score
                        val += _action_score(action, game_state, 0.0)
                    return max(-10.0, min(10.0, val))
        except Exception:
            pass

        if self.model is None or not self.has_torch:
            from cb_agents.heuristic_value import HeuristicValueNetwork
            return HeuristicValueNetwork().evaluate(game_state, action, determinization)

        import torch
        with torch.no_grad():
            try:
                t, z, s, m = self.state_to_card_tokens(game_state)
                if t is not None:
                    t = t.to(self.device); z = z.to(self.device); s = s.to(self.device); m = m.to(self.device)
                    _, val = self.model(x=None, token_ids=t, zone_ids=z, scalars=s, padding_mask=m)
                    return float(val.item())
                else:
                    vec = self.state_to_tensor(game_state)
                    tensor = torch.tensor([vec], dtype=torch.float32, device=self.device)
                    _, val = self.model(tensor)
                    return float(val.item())
            except Exception as e:
                logger.debug(f"Neural evaluation failed: {e}")

        from cb_agents.heuristic_value import HeuristicValueNetwork
        return HeuristicValueNetwork().evaluate(game_state, action, determinization)

    def get_action_priors(self, game_state: dict, candidates: list[str]) -> dict[str, float]:
        if not candidates:
            return {}

        try:
            if hasattr(self, 'inference_client') and self.inference_client and self.inference_client.is_available():
                logits, _ = self.inference_client.evaluate(game_state)
                if logits is not None:
                    import numpy as np
                    try: from cb_agents.data_alignment_helpers import normalize_action
                    except ImportError: from factory.data_alignment_helpers import normalize_action
                    probs = np.exp(logits) / np.sum(np.exp(logits), axis=-1, keepdims=True)
                    priors = {}
                    for action_str in candidates:
                        action_id = normalize_action(action_str, offset_play=0, offset_attack=1000, offset_other=2000)
                        priors[action_str] = float(probs[action_id]) if 0 <= action_id < len(probs) else 0.0
                    return priors
        except Exception:
            pass

        if self.model is None or not self.has_torch:
            return {}

        import torch
        try: from cb_agents.data_alignment_helpers import normalize_action
        except ImportError: from factory.data_alignment_helpers import normalize_action
        with torch.no_grad():
            try:
                t, z, s, m = self.state_to_card_tokens(game_state)
                if t is not None:
                    t = t.to(self.device); z = z.to(self.device); s = s.to(self.device); m = m.to(self.device)
                    logits, _ = self.model(x=None, token_ids=t, zone_ids=z, scalars=s, padding_mask=m)
                    probs = torch.softmax(logits, dim=-1).cpu().numpy()[0]
                    priors = {}
                    for action_str in candidates:
                        action_id = normalize_action(action_str, offset_play=0, offset_attack=1000, offset_other=2000)
                        priors[action_str] = float(probs[action_id]) if 0 <= action_id < len(probs) else 0.0
                    return priors
            except Exception as e:
                logger.debug(f"Action prior calculation failed: {e}")
                return {}
        return {}
