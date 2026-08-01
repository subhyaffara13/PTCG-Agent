
def _allowed_routes_check(user_route: str, allowed_routes: list) -> bool:
    """
    Return if a user is allowed to access route. Helper function for `allowed_routes_check`.

    Parameters:
    - user_route: str - the route the user is trying to call
    - allowed_routes: List[str|LiteLLMRoutes] - the list of allowed routes for the user.
    """
    from starlette.routing import compile_path

    for allowed_route in allowed_routes:
        if allowed_route in LiteLLMRoutes.__members__:
            for template in LiteLLMRoutes[allowed_route].value:
                regex, _, _ = compile_path(template)
                if regex.match(user_route):
                    return True
        elif allowed_route == user_route:
            return True
    return False

