
def _get_model_from_request_context(
    request_data: dict,
    route: str,
    request: Optional[Request],
    llm_router: Optional[Any] = None,
) -> Optional[Union[str, List[str]]]:
    return get_model_from_request(
        request_data=request_data,
        route=route,
        request_headers=_safe_get_request_headers(request=request),
        request_query_params=_safe_get_request_query_params(request=request),
        llm_router=llm_router,
    )

