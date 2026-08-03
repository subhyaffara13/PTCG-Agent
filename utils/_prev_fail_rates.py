from typing import Any, Dict

def _prev_fail_rates(metrics_prev: Any, id_attr: str) -> Dict[str, float]:
    prev_agg_raw: Dict[str, Dict[str, int]] = {}
    for m in metrics_prev:
        gid = getattr(m, id_attr)
        r, b = int(m.requests_evaluated or 0), int(m.blocked_count or 0)
        if gid not in prev_agg_raw:
            prev_agg_raw[gid] = {"req": 0, "blocked": 0}
        prev_agg_raw[gid]["req"] += r
        prev_agg_raw[gid]["blocked"] += b
    return {
        gid: (100.0 * v["blocked"] / v["req"]) if v["req"] else 0.0
        for gid, v in prev_agg_raw.items()
    }

