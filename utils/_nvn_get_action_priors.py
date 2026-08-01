
def _nvn_get_action_priors(self, game_state, candidates):
    if not candidates: return {}
    try:
        if hasattr(self, 'inference_client') and self.inference_client and self.inference_client.is_available():
            logits, _ = self.inference_client.evaluate(game_state)
            if logits is not None:
                import numpy as np
                try: from cb_agents.data_alignment_helpers import normalize_action
                except ImportError: from factory.data_alignment_helpers import normalize_action
                probs = np.exp(logits) / np.sum(np.exp(logits), axis=-1, keepdims=True)
                return {a: float(probs[normalize_action(a, offset_play=0, offset_attack=1000, offset_other=2000)] if 0 <= normalize_action(a, offset_play=0, offset_attack=1000, offset_other=2000) < len(probs) else 0.0) for a in candidates}
    except Exception: pass
    if self.model is None or not self.has_torch: return {}
    import torch
    try: from cb_agents.data_alignment_helpers import normalize_action
    except ImportError: from factory.data_alignment_helpers import normalize_action
    with torch.no_grad():
        try:
            t, z, s, m = self.state_to_card_tokens(game_state)
            if t is not None:
                t = t.to(self.device); z = z.to(self.device); s = s.to(self.device); m = m.to(self.device)
                logits, value = self.model(x=None, token_ids=t, zone_ids=z, scalars=s, padding_mask=m)
            else:
                tensor = self.state_to_tensor(game_state)
                if tensor is not None: logits, value = self.model(x=tensor.to(self.device))
                else: return {}
            probs = torch.softmax(logits.squeeze(0), dim=-1).cpu().numpy()
            return {a: float(probs[normalize_action(a, offset_play=0, offset_attack=1000, offset_other=2000)] if 0 <= normalize_action(a, offset_play=0, offset_attack=1000, offset_other=2000) < len(probs) else 0.0) for a in candidates}
        except Exception as e:
            logger.error(f"Neural action prior extraction failed: {e}")
            return {}


def _nvn_get_action_priors(self, game_state, candidates):
    if not candidates: return {}
    try:
        if hasattr(self, 'inference_client') and self.inference_client and self.inference_client.is_available():
            logits, _ = self.inference_client.evaluate(game_state)
            if logits is not None:
                import numpy as np
                try: from cb_agents.data_alignment_helpers import normalize_action
                except ImportError: from factory.data_alignment_helpers import normalize_action
                probs = np.exp(logits) / np.sum(np.exp(logits), axis=-1, keepdims=True)
                return {a: float(probs[normalize_action(a, offset_play=0, offset_attack=1000, offset_other=2000)] if 0 <= normalize_action(a, offset_play=0, offset_attack=1000, offset_other=2000) < len(probs) else 0.0) for a in candidates}
    except Exception: pass
    if self.model is None or not self.has_torch: return {}
    import torch
    try: from cb_agents.data_alignment_helpers import normalize_action
    except ImportError: from factory.data_alignment_helpers import normalize_action
    with torch.no_grad():
        try:
            t, z, s, m = self.state_to_card_tokens(game_state)
            if t is not None:
                t = t.to(self.device); z = z.to(self.device); s = s.to(self.device); m = m.to(self.device)
                logits, value = self.model(x=None, token_ids=t, zone_ids=z, scalars=s, padding_mask=m)
            else:
                tensor = self.state_to_tensor(game_state)
                if tensor is not None: logits, value = self.model(x=tensor.to(self.device))
                else: return {}
            probs = torch.softmax(logits.squeeze(0), dim=-1).cpu().numpy()
            return {a: float(probs[normalize_action(a, offset_play=0, offset_attack=1000, offset_other=2000)] if 0 <= normalize_action(a, offset_play=0, offset_attack=1000, offset_other=2000) < len(probs) else 0.0) for a in candidates}
        except Exception as e:
            logger.error(f"Neural action prior extraction failed: {e}")
            return {}

