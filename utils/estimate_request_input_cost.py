
def estimate_request_input_cost(
    request_body: dict,
    route: str,
    llm_router: Router | None,
) -> float | None:
    """Cost of the request's input tokens alone.

    Once the provider request is dispatched the input tokens are billed even if
    the client disconnects before the first chunk, so this is the cost floor a
    cancelled in-flight request has already incurred. A cancelled reservation is
    reconciled to this instead of being refunded to zero.
    """
    model = get_model_from_request(request_body, route, llm_router=llm_router)
    if model is None:
        return None

    models = [model] if isinstance(model, str) else model
    estimates = [
        _estimate_request_input_cost_for_model(
            request_body=request_body,
            route=route,
            model=model_name,
            llm_router=llm_router,
        )
        for model_name in models
    ]
    estimates = [estimate for estimate in estimates if estimate is not None]
    if not estimates:
        return None
    return max(cast("list[float]", estimates))

