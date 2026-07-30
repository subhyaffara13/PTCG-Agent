from . import Any, gs_hash, logger, os, torch
from .__getattr___actionprior_basevaluenetwork import BaseValueNetwork

class PPOValueNetwork(BaseValueNetwork):
    model: Any
    device: Any
    _state_to_tensor: Any
    _state_to_card_tokens: Any
    _has_torch: Any
    _cache: Any
    inference_client: Any

    def __init__(self, model_path="models/ppo_actor_critic.pt", device="cpu"):
        self.model = None
        self.device = device
        self._state_to_tensor = None
        self._state_to_card_tokens = None
        self._has_torch = False
        
        # Initialize TCP InferenceClient
        try:
            from factory.inference_client import InferenceClient
            host = os.environ.get("MASTER_HOST", "127.0.0.1")
            self.inference_client = InferenceClient(host=host, port=9999)
        except Exception:
            self.inference_client = None

        try:
            import torch as _
        except ImportError:
            logger.info("PyTorch not available. PPOValueNetwork will use heuristic fallback.")
            return

        from cb_agents.value_network_helpers import state_to_tensor, state_to_card_tokens, HAS_TORCH
        from factory.ppo_trainer_network import ActorCritic
        from factory.state_dimensions import STATE_DIM

        self._has_torch = HAS_TORCH
        self._state_to_tensor = state_to_tensor
        self._state_to_card_tokens = state_to_card_tokens
        self._cache = {}

        if not HAS_TORCH:
            logger.info("Torch helpers unavailable. PPOValueNetwork using heuristic fallback.")
            return

        if not os.path.exists(model_path):
            logger.info(f"PPO model not found at {model_path}. Using heuristic value fallback.")
            return

        try:
            import torch
            ac: Any = ActorCritic(input_dim=STATE_DIM, hidden_dim=256, action_dim=3000)
            ac.load_state_dict(torch.load(model_path, map_location=self.device, weights_only=True))
            ac.to(self.device)
            ac.eval()
            self.model = ac
            logger.info(f"Loaded PPO value network from {model_path}")
        except Exception as e:
            logger.warning(f"PPO value load failed: {e}. Using heuristic fallback.")

    def evaluate(self, game_state: dict, action: str | None = None, determinization: dict | None = None) -> float:
        if game_state.get("game_over"):
            return 1.0 if game_state.get("winner") == "me" else -1.0

        from cb_agents.heuristic_value import HeuristicValueNetwork

        h = gs_hash(game_state)
        cache_key = (h, action)
        if h != 0 and cache_key in self._cache:
            return self._cache[cache_key]

        # Try batched inference server first
        try:
            if hasattr(self, 'inference_client') and self.inference_client and self.inference_client.is_available():
                _, val = self.inference_client.evaluate(game_state)
                if val is not None:
                    if action:
                        from cb_agents.heuristic_pipeline import _action_score
                        val += _action_score(action, game_state, 0.0)
                    res = max(-10.0, min(10.0, val))
                    if h != 0:
                        self._cache[cache_key] = res
                    return res
        except Exception:
            pass

        if self.model is None or not self._has_torch:
            res = HeuristicValueNetwork().evaluate(game_state, action, determinization)
            if h != 0:
                self._cache[cache_key] = res
            return res

        import torch
        with torch.no_grad():
            try:
                t, z, s, m = self._state_to_card_tokens(game_state)
                if t is not None:
                    t = t.to(self.device)
                    z = z.to(self.device)
                    s = s.to(self.device)
                    m = m.to(self.device)
                    _, val = self.model(x=None, token_ids=t, zone_ids=z, scalars=s, padding_mask=m)
                else:
                    tensor = self._state_to_tensor(game_state)
                    if tensor is not None:
                        tensor = tensor.to(self.device)
                        _, val = self.model(x=tensor)
                    else:
                        res = HeuristicValueNetwork().evaluate(game_state, action, determinization)
                        if h != 0:
                            self._cache[cache_key] = res
                        return res

                v = val.item()
                if action:
                    from cb_agents.heuristic_pipeline import _action_score
                    v += _action_score(action, game_state, 0.0)
                res = max(-10.0, min(10.0, v))
                if h != 0:
                    self._cache[cache_key] = res
                return res

            except Exception as e:
                logger.error(f"PPO value inference failed: {e}")
                res = HeuristicValueNetwork().evaluate(game_state, action, determinization)
                if h != 0:
                    self._cache[cache_key] = res
                return res

