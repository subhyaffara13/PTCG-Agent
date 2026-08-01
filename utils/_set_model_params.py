
def _set_model_params(span: "Span", model_params: Optional[dict], span_attrs) -> None:
    if not model_params:
        return

    safe_set_attribute(
        span, span_attrs.LLM_INVOCATION_PARAMETERS, safe_dumps(model_params)
    )
    if model_params.get("user"):
        user_id = model_params.get("user")
        if user_id is not None:
            safe_set_attribute(span, span_attrs.USER_ID, user_id)

