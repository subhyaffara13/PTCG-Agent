from typing import List, Optional, Tuple

def _check_valid_ip(
    allowed_ips: Optional[List[str]],
    request: Request,
    use_x_forwarded_for: Optional[bool] = False,
) -> Tuple[bool, Optional[str]]:
    """
    Returns if ip is allowed or not
    """
    if allowed_ips is None:  # if not set, assume true
        return True, None

    # if general_settings.get("use_x_forwarded_for") is True then use x-forwarded-for
    client_ip = _get_request_ip_address(
        request=request, use_x_forwarded_for=use_x_forwarded_for
    )

    # Check if IP address is allowed
    if client_ip not in allowed_ips:
        return False, client_ip

    return True, client_ip

