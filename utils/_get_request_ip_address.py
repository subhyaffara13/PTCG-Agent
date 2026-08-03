from typing import Optional

def _get_request_ip_address(
    request: Request, use_x_forwarded_for: Optional[bool] = False
) -> Optional[str]:
    client_ip = None
    if use_x_forwarded_for is True and "x-forwarded-for" in request.headers:
        client_ip = request.headers["x-forwarded-for"]
    elif request.client is not None:
        client_ip = request.client.host
    else:
        client_ip = ""

    return client_ip

