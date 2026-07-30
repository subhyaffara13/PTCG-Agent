from . import gs_hash, logger, torch

def _pvn_evaluate_state(self, game_state, action, determinization):
    if game_state.get("game_over"):
        return 1.0 if game_state.get("winner") == "me" else -1.0
    from cb_agents.heuristic_value import HeuristicValueNetwork
    h = gs_hash(game_state); cache_key = (h, action)
    if h != 0 and cache_key in self._cache: return self._cache[cache_key]
    try:
        if hasattr(self, 'inference_client') and self.inference_client and self.inference_client.is_available():
            _, val = self.inference_client.evaluate(game_state)
            if val is not None:
                if action:
                    from cb_agents.heuristic_pipeline import _action_score
                    val += _action_score(action, game_state, 0.0)
                res = max(-10.0, min(10.0, val))
                if h != 0: self._cache[cache_key] = res
                return res
    except Exception: pass
    if self.model is None or not self._has_torch:
        res = HeuristicValueNetwork().evaluate(game_state, action, determinization)
        if h != 0: self._cache[cache_key] = res
        return res
    import torch
    with torch.no_grad():
        try:
            t, z, s, m = self._state_to_card_tokens(game_state)
            if t is not None:
                t = t.to(self.device); z = z.to(self.device); s = s.to(self.device); m = m.to(self.device)
                _, val = self.model(x=None, token_ids=t, zone_ids=z, scalars=s, padding_mask=m)
            else:
                tensor = self._state_to_tensor(game_state)
                if tensor is not None: _, val = self.model(x=tensor.to(self.device))
                else:
                    res = HeuristicValueNetwork().evaluate(game_state, action, determinization)
                    if h != 0: self._cache[cache_key] = res; return res
            v = val.item()
            if action:
                from cb_agents.heuristic_pipeline import _action_score
                v += _action_score(action, game_state, 0.0)
            res = max(-10.0, min(10.0, v))
            if h != 0: self._cache[cache_key] = res
            return res
        except Exception as e:
            logger.error(f"PPO value inference failed: {e}")
            res = HeuristicValueNetwork().evaluate(game_state, action, determinization)
            if h != 0: self._cache[cache_key] = res
            return res
