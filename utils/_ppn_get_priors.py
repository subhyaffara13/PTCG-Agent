
def _ppn_get_priors(self, game_state, legal_actions):
    if not legal_actions: return []
    h = gs_hash(game_state)
    if h != 0 and h in self._cache: return self._cache[h]
    try:
        if hasattr(self, 'inference_client') and self.inference_client and self.inference_client.is_available():
            logits, _ = self.inference_client.evaluate(game_state)
            if logits is not None:
                import numpy as np
                try: from cb_agents.data_alignment_helpers import normalize_action
                except ImportError: from factory.data_alignment_helpers import normalize_action
                probs = np.exp(logits) / np.sum(np.exp(logits), axis=-1, keepdims=True)
                priors = [ActionPrior(action=a, prob=float(probs[normalize_action(a, offset_play=0, offset_attack=1000, offset_other=2000)]) if 0 <= normalize_action(a, offset_play=0, offset_attack=1000, offset_other=2000) < len(probs) else 0.0) for a in legal_actions]
                total = sum(p.prob for p in priors)
                if total > 0:
                    for p in priors: p.prob /= total
                if h != 0: self._cache[h] = priors
                return priors
    except Exception: pass
    if self.model is None or not self._has_torch: return self._heuristic_fallback.get_priors(game_state, legal_actions)
    import torch
    try: from cb_agents.data_alignment_helpers import normalize_action
    except ImportError: from factory.data_alignment_helpers import normalize_action
    with torch.no_grad():
        try:
            t, z, s, m = self._state_to_card_tokens(game_state)
            if t is not None:
                t = t.to(self.device); z = z.to(self.device); s = s.to(self.device); m = m.to(self.device)
                logits, _ = self.model(x=None, token_ids=t, zone_ids=z, scalars=s, padding_mask=m)
            else:
                tensor = self._state_to_tensor(game_state)
                if tensor is not None: logits, _ = self.model(x=tensor.to(self.device))
                else: return self._heuristic_fallback.get_priors(game_state, legal_actions)
            probs = torch.softmax(logits.squeeze(0), dim=-1).cpu().numpy()
            priors = []
            for action_str in legal_actions:
                action_id = normalize_action(action_str, offset_play=0, offset_attack=1000, offset_other=2000)
                priors.append(ActionPrior(action=action_str, prob=float(probs[action_id]) if 0 <= action_id < len(probs) else 0.0))
            total = sum(p.prob for p in priors)
            if total > 0:
                for p in priors: p.prob /= total
            if h != 0: self._cache[h] = priors
            return priors
        except Exception as e:
            logger.error(f"PPO policy inference failed: {e}")
            return self._heuristic_fallback.get_priors(game_state, legal_actions)


def _ppn_get_priors(self, game_state, legal_actions):
    if not legal_actions: return []
    h = gs_hash(game_state)
    if h != 0 and h in self._cache: return self._cache[h]
    try:
        if hasattr(self, 'inference_client') and self.inference_client and self.inference_client.is_available():
            logits, _ = self.inference_client.evaluate(game_state)
            if logits is not None:
                import numpy as np
                try: from cb_agents.data_alignment_helpers import normalize_action
                except ImportError: from factory.data_alignment_helpers import normalize_action
                probs = np.exp(logits) / np.sum(np.exp(logits), axis=-1, keepdims=True)
                priors = [ActionPrior(action=a, prob=float(probs[normalize_action(a, offset_play=0, offset_attack=1000, offset_other=2000)]) if 0 <= normalize_action(a, offset_play=0, offset_attack=1000, offset_other=2000) < len(probs) else 0.0) for a in legal_actions]
                total = sum(p.prob for p in priors)
                if total > 0:
                    for p in priors: p.prob /= total
                if h != 0: self._cache[h] = priors
                return priors
    except Exception: pass
    if self.model is None or not self._has_torch: return self._heuristic_fallback.get_priors(game_state, legal_actions)
    import torch
    try: from cb_agents.data_alignment_helpers import normalize_action
    except ImportError: from factory.data_alignment_helpers import normalize_action
    with torch.no_grad():
        try:
            t, z, s, m = self._state_to_card_tokens(game_state)
            if t is not None:
                t = t.to(self.device); z = z.to(self.device); s = s.to(self.device); m = m.to(self.device)
                logits, _ = self.model(x=None, token_ids=t, zone_ids=z, scalars=s, padding_mask=m)
            else:
                tensor = self._state_to_tensor(game_state)
                if tensor is not None: logits, _ = self.model(x=tensor.to(self.device))
                else: return self._heuristic_fallback.get_priors(game_state, legal_actions)
            probs = torch.softmax(logits.squeeze(0), dim=-1).cpu().numpy()
            priors = []
            for action_str in legal_actions:
                action_id = normalize_action(action_str, offset_play=0, offset_attack=1000, offset_other=2000)
                priors.append(ActionPrior(action=action_str, prob=float(probs[action_id]) if 0 <= action_id < len(probs) else 0.0))
            total = sum(p.prob for p in priors)
            if total > 0:
                for p in priors: p.prob /= total
            if h != 0: self._cache[h] = priors
            return priors
        except Exception as e:
            logger.error(f"PPO policy inference failed: {e}")
            return self._heuristic_fallback.get_priors(game_state, legal_actions)

