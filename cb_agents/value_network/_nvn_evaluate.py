from . import logger, torch

def _nvn_evaluate_impl(self, game_state, action, determinization):
    if game_state.get("game_over"):
        return 1.0 if game_state.get("winner") == "me" else -1.0
    try:
        if hasattr(self, 'inference_client') and self.inference_client and self.inference_client.is_available():
            _, val = self.inference_client.evaluate(game_state)
            if val is not None:
                if action:
                    from cb_agents.heuristic_pipeline import _action_score
                    val += _action_score(action, game_state, 0.0)
                return max(-10.0, min(10.0, val))
    except Exception: pass
    if self.model is None or not self.has_torch:
        from cb_agents.heuristic_value import HeuristicValueNetwork
        return HeuristicValueNetwork().evaluate(game_state, action, determinization)
    import torch
    with torch.no_grad():
        try:
            t, z, s, m = self.state_to_card_tokens(game_state)
            if t is not None:
                t = t.to(self.device); z = z.to(self.device); s = s.to(self.device); m = m.to(self.device)
                _, value = self.model(x=None, token_ids=t, zone_ids=z, scalars=s, padding_mask=m)
                val = value.item()
            else:
                tensor = self.state_to_tensor(game_state)
                if tensor is not None:
                    _, value = self.model(x=tensor.to(self.device)); val = value.item()
                else: val = 0.0
            if action:
                from cb_agents.heuristic_pipeline import _action_score
                val += _action_score(action, game_state, 0.0)
            return max(-10.0, min(10.0, val))
        except Exception as e:
            logger.error(f"Neural evaluation failed: {e}")
    from cb_agents.heuristic_value import HeuristicValueNetwork
    return HeuristicValueNetwork().evaluate(game_state, action, determinization)
