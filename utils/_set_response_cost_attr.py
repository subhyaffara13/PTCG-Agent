
def _set_response_cost_attr(span: "Span", standard_logging_payload) -> None:
    """Emit cost attributes from the StandardLoggingPayload when present.

    Uses the OpenInference `llm.cost.total` key so Arize / Phoenix can
    surface the cost in their "Total Cost" column. LiteLLM only tracks a
    single total in `StandardLoggingPayload.response_cost`, so we cannot
    split it into prompt/completion. We also keep the legacy
    `llm.response.cost` key for back-compat with any consumer querying it.
    """
    if not isinstance(standard_logging_payload, dict):
        return
    cost = standard_logging_payload.get("response_cost")
    if cost is None:
        return
    try:
        cost_value = float(cost)
    except (TypeError, ValueError):
        return
    safe_set_attribute(span, "llm.cost.total", cost_value)
    safe_set_attribute(span, "llm.response.cost", cost_value)

