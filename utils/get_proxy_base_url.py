import os
from typing import Optional

def get_proxy_base_url() -> Optional[str]:
    """
    Get the proxy base url from the environment variables.
    """
    return os.getenv("PROXY_BASE_URL")

