
def _enforce_user_param_check(
    general_settings: dict, request: Request, request_body: dict, route: str
) -> None:
    if not general_settings.get("enforce_user_param", False):
        return

    http_method = request.method if hasattr(request, "method") else None
    is_post_method = http_method and http_method.upper() == "POST"
    is_openai_route = RouteChecks.is_llm_api_route(route=route)
    is_mcp_route = (
        route in LiteLLMRoutes.mcp_routes.value
        or RouteChecks.check_route_access(
            route=route, allowed_routes=LiteLLMRoutes.mcp_routes.value
        )
    )

    if (
        is_post_method
        and is_openai_route
        and not is_mcp_route
        and "user" not in request_body
    ):
        raise Exception(
            f"'user' param not passed in. 'enforce_user_param'={general_settings['enforce_user_param']}"
        )

