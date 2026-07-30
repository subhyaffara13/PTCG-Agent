from . import Any, List, gs_hash, logger, os, torch
from .__getattr___actionprior_basevaluenetwork import ActionPrior
from .basepolicynetwork_heuristicpolicynetwork import BasePolicyNetwork, HeuristicPolicyNetwork

class PPOPolicyNetwork(BasePolicyNetwork):
    model: Any
    device: Any
    _state_to_tensor: Any
    _state_to_card_tokens: Any
    _has_torch: Any
    _heuristic_fallback: Any
    _cache: Any
    inference_client: Any

    def __init__(self, model_path="models/ppo_actor_critic.pt", device="cpu"):
        self.model = None
        self.device = device
        self._state_to_tensor = None
        self._state_to_card_tokens = None
        self._has_torch = False
        self._heuristic_fallback = HeuristicPolicyNetwork()
        self._cache = {}
        
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
            logger.info("PyTorch not available. PPOPolicyNetwork will use heuristic fallback.")
            return

        from cb_agents.value_network_helpers import state_to_tensor, state_to_card_tokens, HAS_TORCH
        from factory.ppo_trainer_network import ActorCritic
        from factory.state_dimensions import STATE_DIM

        self._has_torch = HAS_TORCH
        self._state_to_tensor = state_to_tensor
        self._state_to_card_tokens = state_to_card_tokens

        if not HAS_TORCH:
            logger.info("Torch helpers unavailable. PPOPolicyNetwork using heuristic fallback.")
            return

        if not os.path.exists(model_path):
            logger.info(f"PPO model not found at {model_path}. Using heuristic policy fallback.")
            return

        try:
            import torch
            ac: Any = ActorCritic(input_dim=STATE_DIM, hidden_dim=256, action_dim=3000)
            ac.load_state_dict(torch.load(model_path, map_location=self.device, weights_only=True))
            ac.to(self.device)
            ac.eval()
            self.model = ac
            logger.info(f"Loaded PPO policy network from {model_path}")
            
            # Dynamically export to ONNX if it doesn't exist yet
            onnx_path = model_path.replace(".pt", ".onnx")
            if not os.path.exists(onnx_path):
                try:
                    import torch.onnx
                    import contextlib
                    import io
                    
                    class ONNXExportWrapper(torch.nn.Module):
                        def __init__(self, model):
                            super().__init__()
                            self.model = model
                        def forward(self, token_ids, zone_ids, scalars, padding_mask):
                            return self.model(x=None, token_ids=token_ids, zone_ids=zone_ids, scalars=scalars, padding_mask=padding_mask)
                            
                    wrapper = ONNXExportWrapper(ac)
                    dummy_token_ids = torch.zeros(1, 32, dtype=torch.long, device=self.device)
                    dummy_zone_ids = torch.zeros(1, 32, dtype=torch.long, device=self.device)
                    dummy_scalars = torch.zeros(1, 6, dtype=torch.float32, device=self.device)
                    dummy_padding_mask = torch.zeros(1, 33, dtype=torch.bool, device=self.device)
                    
                    # torch.onnx.export tries to print a \u274c (red cross emoji) on warnings,
                    # which crashes the default Windows charmap encoder. We silence it here.
                    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                        torch.onnx.export(
                            wrapper,
                            (dummy_token_ids, dummy_zone_ids, dummy_scalars, dummy_padding_mask),
                            onnx_path,
                            input_names=["token_ids", "zone_ids", "scalars", "padding_mask"],
                            output_names=["logits", "value"],
                            dynamic_axes={
                                "token_ids": {0: "batch_size"},
                                "zone_ids": {0: "batch_size"},
                                "scalars": {0: "batch_size"},
                                "padding_mask": {0: "batch_size"},
                                "logits": {0: "batch_size"},
                                "value": {0: "batch_size"}
                            },
                            opset_version=14
                        )
                    logger.info(f"Dynamically exported ONNX model to {onnx_path}")
                except Exception as ex:
                    logger.warning(f"Dynamic ONNX export failed: {ex}")
        except Exception as e:
            logger.warning(f"PPO policy load failed: {e}. Using heuristic fallback.")

    def get_priors(self, game_state: dict, legal_actions: List[str]) -> List[ActionPrior]:
        if not legal_actions:
            return []

        h = gs_hash(game_state)
        if h != 0 and h in self._cache:
            return self._cache[h]

        # Try batched inference server first
        try:
            if hasattr(self, 'inference_client') and self.inference_client and self.inference_client.is_available():
                logits, _ = self.inference_client.evaluate(game_state)
                if logits is not None:
                    import numpy as np
                    from factory.data_alignment_helpers import normalize_action
                    probs = np.exp(logits) / np.sum(np.exp(logits), axis=-1, keepdims=True)
                    priors = []
                    for action_str in legal_actions:
                        action_id = normalize_action(action_str, offset_play=0, offset_attack=1000, offset_other=2000)
                        prob = float(probs[action_id]) if 0 <= action_id < len(probs) else 0.0
                        priors.append(ActionPrior(action=action_str, prob=prob))
                    total = sum(p.prob for p in priors)
                    if total > 0:
                        for p in priors:
                            p.prob /= total
                    if h != 0:
                        self._cache[h] = priors
                    return priors
        except Exception:
            pass

        if self.model is None or not self._has_torch:
            return self._heuristic_fallback.get_priors(game_state, legal_actions)

        import torch
        from factory.data_alignment_helpers import normalize_action

        with torch.no_grad():
            try:
                t, z, s, m = self._state_to_card_tokens(game_state)
                if t is not None:
                    t = t.to(self.device)
                    z = z.to(self.device)
                    s = s.to(self.device)
                    m = m.to(self.device)
                    logits, _ = self.model(x=None, token_ids=t, zone_ids=z, scalars=s, padding_mask=m)
                else:
                    tensor = self._state_to_tensor(game_state)
                    if tensor is not None:
                        tensor = tensor.to(self.device)
                        logits, _ = self.model(x=tensor)
                    else:
                        return self._heuristic_fallback.get_priors(game_state, legal_actions)

                probs = torch.softmax(logits.squeeze(0), dim=-1).cpu().numpy()

                priors = []
                for action_str in legal_actions:
                    action_id = normalize_action(action_str, offset_play=0, offset_attack=1000, offset_other=2000)
                    prob = float(probs[action_id]) if 0 <= action_id < len(probs) else 0.0
                    priors.append(ActionPrior(action=action_str, prob=prob))

                total = sum(p.prob for p in priors)
                if total > 0:
                    for p in priors:
                        p.prob /= total
                if h != 0:
                    self._cache[h] = priors
                return priors

            except Exception as e:
                logger.error(f"PPO policy inference failed: {e}")
                return self._heuristic_fallback.get_priors(game_state, legal_actions)

