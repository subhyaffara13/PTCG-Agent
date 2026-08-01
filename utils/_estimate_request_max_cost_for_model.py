
def _estimate_request_max_cost_for_model(
    request_body: dict,
    route: str,
    model: str,
    llm_router: Optional[Router],
) -> Optional[float]:
    model_info = _get_model_cost_info(model=model, llm_router=llm_router)
    if model_info is None:
        return None

    image_cost = _estimate_image_generation_cost(
        request_body=request_body,
        model_info=model_info,
    )
    if image_cost is not None:
        return image_cost

    input_cost_per_token = _to_float(model_info.get("input_cost_per_token"))
    output_cost_per_token = _to_float(model_info.get("output_cost_per_token"))
    input_tokens = _estimate_input_tokens(
        request_body=request_body,
        route=route,
        model=model,
        model_info=model_info,
    )
    output_tokens = _estimate_output_tokens(
        request_body=request_body,
        route=route,
        model_info=model_info,
    )
    if input_tokens is None or output_tokens is None:
        return None

    cost = 0.0
    if input_cost_per_token is not None:
        cost += input_tokens * input_cost_per_token
    elif input_tokens > 0:
        return None

    output_multiplier = _get_output_multiplier(request_body=request_body)
    if output_cost_per_token is not None:
        cost += output_tokens * output_multiplier * output_cost_per_token
    elif output_tokens > 0:
        return None

    return cost

