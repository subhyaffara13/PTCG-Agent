
def _guardrail_overview_rows(
    guardrails: Any,
    agg: Dict[str, Dict[str, Any]],
    prev_agg: Dict[str, float],
) -> List[UsageOverviewRow]:
    rows: List[UsageOverviewRow] = []
    covered_keys: set = set()
    for g in guardrails:
        gid, display_name = _get_guardrail_attrs(g)
        # Metrics are keyed by logical name from spend log metadata; guardrails table uses UUID
        lookup_keys = [k for k in (display_name, gid) if k]
        covered_keys.update(lookup_keys)
        a = {"requests": 0, "passed": 0, "blocked": 0, "flagged": 0}
        for k in lookup_keys:
            if k in agg:
                a = agg[k]
                break
        req, blocked = a["requests"], a["blocked"]
        fail_rate = (100.0 * blocked / req) if req else 0.0
        litellm_params = (
            (g.litellm_params or {}) if isinstance(g.litellm_params, dict) else {}
        )
        provider = str(litellm_params.get("guardrail", "Unknown"))
        guardrail_info = (
            (g.guardrail_info or {}) if isinstance(g.guardrail_info, dict) else {}
        )
        gtype = str(guardrail_info.get("type", "Guardrail"))
        prev_fail = 0.0
        for k in lookup_keys:
            if k in prev_agg:
                prev_fail = float(prev_agg.get(k, 0.0) or 0.0)
                break
        trend = _trend_from_comparison(fail_rate, prev_fail)
        rows.append(
            UsageOverviewRow(
                id=gid,
                name=display_name or str(gid),
                type=gtype,
                provider=provider,
                requestsEvaluated=req,
                failRate=round(fail_rate, 1),
                avgScore=None,
                avgLatency=None,
                status=_status_from_fail_rate(fail_rate),
                trend=trend,
            )
        )
    # Add rows for guardrails with metrics but not in guardrails table (e.g. MCP, config)
    for agg_key, a in agg.items():
        if agg_key in covered_keys or a["requests"] == 0:
            continue
        req, blocked = a["requests"], a["blocked"]
        fail_rate = (100.0 * blocked / req) if req else 0.0
        prev_fail = float(prev_agg.get(agg_key, 0.0) or 0.0)
        trend = _trend_from_comparison(fail_rate, prev_fail)
        rows.append(
            UsageOverviewRow(
                id=agg_key,
                name=agg_key,
                type="Guardrail",
                provider="Custom",
                requestsEvaluated=req,
                failRate=round(fail_rate, 1),
                avgScore=None,
                avgLatency=None,
                status=_status_from_fail_rate(fail_rate),
                trend=trend,
            )
        )
    return rows

