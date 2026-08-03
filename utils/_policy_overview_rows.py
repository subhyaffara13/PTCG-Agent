from typing import Any, Dict, List

def _policy_overview_rows(
    policies: Any,
    agg: Dict[str, Dict[str, Any]],
    prev_agg: Dict[str, float],
) -> List[UsageOverviewRow]:
    rows: List[UsageOverviewRow] = []
    for p in policies:
        pid = p.policy_id
        a = agg.get(pid, {"requests": 0, "passed": 0, "blocked": 0, "flagged": 0})
        req, blocked = a["requests"], a["blocked"]
        fail_rate = (100.0 * blocked / req) if req else 0.0
        trend = _trend_from_comparison(fail_rate, prev_agg.get(pid, 0.0))
        rows.append(
            UsageOverviewRow(
                id=pid,
                name=p.policy_name or pid,
                type="Policy",
                provider="LiteLLM",
                requestsEvaluated=req,
                failRate=round(fail_rate, 1),
                avgScore=None,
                avgLatency=None,
                status=_status_from_fail_rate(fail_rate),
                trend=trend,
            )
        )
    return rows

