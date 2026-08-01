
def join_paths(base_path: str, route: str) -> str:
    # Remove trailing slashes from base_path and leading slashes from route
    base_path = base_path.rstrip("/")
    route = route.lstrip("/")

    # If base_path is empty, return route with leading slash
    if not base_path:
        return f"/{route}" if route else "/"

    # If route is empty, return just base_path
    if not route:
        return base_path

    # Check if base_path already ends with the route to avoid duplication
    if base_path.endswith(f"/{route}"):
        final_path = base_path
    else:
        # Join with single slash
        final_path = f"{base_path}/{route}"

    return final_path

