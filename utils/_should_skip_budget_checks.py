
def _should_skip_budget_checks(
    request_data: dict,
    route: str,
    request: Optional[Request],
    llm_router: Optional[Any],
) -> bool:
    model = _get_model_from_request_context(
        request_data=request_data,
        route=route,
        request=request,
        llm_router=llm_router,
    )
    if model is not None and llm_router is not None:
        return _is_model_cost_zero(model=model, llm_router=llm_router)
    return False

