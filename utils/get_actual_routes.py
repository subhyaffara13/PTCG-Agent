
def get_actual_routes(allowed_routes: list) -> list:
    actual_routes: list = []
    for route_name in allowed_routes:
        try:
            route_value = LiteLLMRoutes[route_name].value
            if isinstance(route_value, set):
                actual_routes.extend(list(route_value))
            else:
                actual_routes.extend(route_value)

        except KeyError:
            actual_routes.append(route_name)
    return actual_routes

