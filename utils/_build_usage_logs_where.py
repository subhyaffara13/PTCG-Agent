from typing import Any, Dict, List, Optional

def _build_usage_logs_where(
    guardrail_ids: Optional[List[str]],
    policy_id: Optional[str],
    start_date: Optional[str],
    end_date: Optional[str],
) -> Dict[str, Any]:
    where: Dict[str, Any] = {}
    if guardrail_ids:
        where["guardrail_id"] = (
            {"in": guardrail_ids} if len(guardrail_ids) > 1 else guardrail_ids[0]
        )
    if policy_id:
        where["policy_id"] = policy_id
    if start_date or end_date:
        st_filter: Dict[str, Any] = {}
        if start_date:
            sd = start_date.replace("Z", "+00:00").strip()
            if "T" not in sd:
                sd += "T00:00:00+00:00"
            st_filter["gte"] = datetime.fromisoformat(sd)
        if end_date:
            ed = end_date.replace("Z", "+00:00").strip()
            if "T" not in ed:
                ed += "T23:59:59+00:00"
            st_filter["lte"] = datetime.fromisoformat(ed)
        where["start_time"] = st_filter
    return where

