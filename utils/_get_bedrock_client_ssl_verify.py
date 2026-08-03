from typing import Union

def _get_bedrock_client_ssl_verify() -> Union[bool, str]:
    """
    Get SSL verification setting for Bedrock client.

    Returns the SSL verification setting which can be:
    - True: Use default SSL verification
    - False: Disable SSL verification
    - str: Path to a custom CA bundle file
    """
    from litellm.llms.custom_httpx.http_handler import get_ssl_verify

    return get_ssl_verify()

