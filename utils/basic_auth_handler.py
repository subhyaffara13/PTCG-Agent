from typing import Callable, List, Optional, Tuple

def basic_auth_handler(
        url: str,
        method: str,
        timeout: Optional[float],
        headers: List[Tuple[str, str]],
        data: bytes,
        username: Optional[str] = None,
        password: Optional[str] = None,
) -> Callable[[], None]:
    """Handler that implements HTTP/HTTPS connections with Basic Auth.

    Sets auth headers using supplied 'username' and 'password', if set.
    Used by the push_to_gateway functions. Can be re-used by other handlers."""

    def handle():
        """Handler that implements HTTP Basic Auth.
        """
        if username is not None and password is not None:
            auth_value = f'{username}:{password}'.encode()
            auth_token = base64.b64encode(auth_value)
            auth_header = b'Basic ' + auth_token
            headers.append(('Authorization', auth_header))
        default_handler(url, method, timeout, headers, data)()

    return handle

