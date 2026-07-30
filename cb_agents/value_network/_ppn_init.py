from . import logger, os, torch

def _ppn_init(self, model_path, device):
    from .__getattr___actionprior_basevaluenetwork import ActionPrior
    from .basepolicynetwork_heuristicpolicynetwork import HeuristicPolicyNetwork
    self.model = None; self.device = device
    self._state_to_tensor = None; self._state_to_card_tokens = None; self._has_torch = False
    self._heuristic_fallback = HeuristicPolicyNetwork(); self._cache = {}
    try:
        from factory.inference_client import InferenceClient
        host = os.environ.get("MASTER_HOST", "127.0.0.1")
        self.inference_client = InferenceClient(host=host, port=9999)
    except Exception: self.inference_client = None
    try: import torch as _
    except ImportError:
        logger.info("PyTorch not available. PPOPolicyNetwork will use heuristic fallback."); return
    from cb_agents.value_network_helpers import state_to_tensor, state_to_card_tokens, HAS_TORCH
    from factory.ppo_trainer_network import ActorCritic
    from factory.state_dimensions import STATE_DIM
    self._has_torch = HAS_TORCH; self._state_to_tensor = state_to_tensor; self._state_to_card_tokens = state_to_card_tokens
    if not HAS_TORCH: return
    if not os.path.exists(model_path): logger.info(f"PPO model not found at {model_path}."); return
    try:
        import torch
        ac = ActorCritic(input_dim=STATE_DIM, hidden_dim=256, action_dim=3000)
        ac.load_state_dict(torch.load(model_path, map_location=self.device, weights_only=True))
        ac.to(self.device); ac.eval(); self.model = ac
        logger.info(f"Loaded PPO policy network from {model_path}")
    except Exception as e: logger.warning(f"PPO policy load failed: {e}. Using heuristic fallback.")
