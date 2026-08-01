
def _estimate_request_input_cost_for_model(
    request_body: dict,
    route: str,
    model: str,
    llm_router: Router | None,
) -> float | None:
    model_info = _get_model_cost_info(model=model, llm_router=llm_router)
    if model_info is None:
        return None
    input_cost_per_token = _to_float(model_info.get("input_cost_per_token"))
    if input_cost_per_token is None:
        return None
    input_tokens = _estimate_input_tokens(
        request_body=request_body,
        route=route,
        model=model,
        model_info=model_info,
    )
    if input_tokens is None:
        return None
    return input_tokens * input_cost_per_token

