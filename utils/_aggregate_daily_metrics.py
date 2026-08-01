
def _aggregate_daily_metrics(metrics: Any, id_attr: str) -> Dict[str, Dict[str, Any]]:
    agg: Dict[str, Dict[str, Any]] = {}
    for m in metrics:
        gid = getattr(m, id_attr)
        if gid not in agg:
            agg[gid] = {"requests": 0, "passed": 0, "blocked": 0, "flagged": 0}
        agg[gid]["requests"] += int(m.requests_evaluated or 0)
        agg[gid]["passed"] += int(m.passed_count or 0)
        agg[gid]["blocked"] += int(m.blocked_count or 0)
        agg[gid]["flagged"] += int(m.flagged_count or 0)
    return agg

