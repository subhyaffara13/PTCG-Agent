import json
from typing import Any, Optional

def _usage_log_entry_from_row(
    r: Any, sl: Any, action_filter: Optional[str]
) -> Optional[UsageLogEntry]:
    meta = sl.metadata
    if isinstance(meta, str):
        try:
            meta = json.loads(meta)
        except Exception:
            meta = {}
    guardrail_info_list = (meta or {}).get("guardrail_information") or []
    entry_for_guardrail = None
    for gi in guardrail_info_list:
        if (gi.get("guardrail_id") or gi.get("guardrail_name")) == r.guardrail_id:
            entry_for_guardrail = gi
            break
    action_val = "passed"
    score_val = None
    latency_val = None
    reason_val = None
    if entry_for_guardrail:
        st = (entry_for_guardrail.get("guardrail_status") or "").lower()
        if "intervened" in st or "block" in st:
            action_val = "blocked"
        elif "fail" in st or "error" in st:
            action_val = "flagged"
        duration = entry_for_guardrail.get("duration")
        if duration is not None:
            latency_val = round(float(duration) * 1000, 0)
        score_val = entry_for_guardrail.get(
            "confidence_score"
        ) or entry_for_guardrail.get("risk_score")
        if score_val is not None:
            score_val = round(float(score_val), 2)
        resp = entry_for_guardrail.get("guardrail_response")
        if isinstance(resp, str):
            reason_val = resp[:500]
        elif isinstance(resp, dict):
            reason_val = str(resp)[:500]
    if action_filter and action_val != action_filter:
        return None
    ts = (
        sl.startTime.isoformat()
        if hasattr(sl.startTime, "isoformat")
        else str(sl.startTime)
    )
    return UsageLogEntry(
        id=r.request_id,
        timestamp=ts,
        action=action_val,
        score=score_val,
        latency_ms=latency_val,
        model=sl.model,
        input_snippet=_input_snippet_for_log(sl),
        output_snippet=_snippet(sl.response),
        reason=reason_val,
    )

