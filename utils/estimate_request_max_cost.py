
def estimate_request_max_cost(
    request_body: dict,
    route: str,
    llm_router: Optional[Router],
) -> Optional[float]:
    model = get_model_from_request(request_body, route, llm_router=llm_router)
    if model is None:
        return None

    models = [model] if isinstance(model, str) else model
    estimates = [
        _estimate_request_max_cost_for_model(
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
    return max(cast(List[float], estimates))

