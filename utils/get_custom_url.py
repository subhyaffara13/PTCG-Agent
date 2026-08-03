from typing import Optional

def get_custom_url(request_base_url: str, route: Optional[str] = None) -> str:
    # Use environment variable value, otherwise use URL from request
    server_base_url = get_proxy_base_url()
    if server_base_url is not None:
        base_url = server_base_url
    else:
        base_url = request_base_url

    server_root_path = get_server_root_path()
    if route is not None:
        if server_root_path != "":
            # First join base_url with server_root_path, then with route
            intermediate_url = join_paths(base_url, server_root_path)
            return join_paths(intermediate_url, route)
        else:
            return join_paths(base_url, route)
    else:
        return join_paths(base_url, server_root_path)

