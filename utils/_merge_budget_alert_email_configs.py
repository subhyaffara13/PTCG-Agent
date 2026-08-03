from typing import Any, Dict, List, Optional

def _merge_budget_alert_email_configs(
    global_cfg: Optional[Dict[str, Any]],
    per_key_cfg: Optional[Dict[str, Any]],
) -> Optional[Dict[str, List[str]]]:
    """
    Per-threshold additive merge: each threshold's recipient list is the union
    of global + per-key entries (deduped, global-first ordering). Missing
    thresholds on one side are inherited from the other.
    """
    global_cfg_normalized = _normalize_alert_emails(global_cfg)
    per_key_cfg_normalized = _normalize_alert_emails(per_key_cfg)
    if not global_cfg_normalized and not per_key_cfg_normalized:
        return None
    thresholds = set(global_cfg_normalized) | set(per_key_cfg_normalized)
    return {
        t: list(
            dict.fromkeys(
                global_cfg_normalized.get(t, []) + per_key_cfg_normalized.get(t, [])
            )
        )
        for t in thresholds
    }

