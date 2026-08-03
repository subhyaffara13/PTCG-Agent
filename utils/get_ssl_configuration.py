import os
from typing import Optional, Union

def get_ssl_configuration(
    ssl_verify: Optional[VerifyTypes] = None,
) -> Union[bool, str, ssl.SSLContext]:
    """
    Unified SSL configuration function that handles ssl_context and ssl_verify logic.

    SSL Configuration Priority:
    1. If ssl_verify is provided -> is a SSL context use the custom SSL context
    2. If ssl_verify is False -> disable SSL verification (ssl=False)
    3. If ssl_verify is a string -> use it as a path to CA bundle file
    4. If SSL_CERT_FILE environment variable is set and exists -> use it as CA bundle file
    5. Else will use default SSL context with certifi CA bundle

    If ssl_security_level is set, it will apply the security level to the SSL context.

    SSL contexts are cached to avoid creating duplicate contexts with the same configuration,
    which reduces memory allocation and improves performance.

    Args:
        ssl_verify: SSL verification setting. Can be:
            - None: Use default from environment/litellm settings
            - False: Disable SSL verification
            - True: Enable SSL verification
            - str: Path to CA bundle file

    Returns:
        Union[bool, str, ssl.SSLContext]: Appropriate SSL configuration
    """
    if isinstance(ssl_verify, ssl.SSLContext):
        # If ssl_verify is already an SSLContext, return it directly
        return ssl_verify

    # Get resolved ssl_verify
    ssl_verify = get_ssl_verify(ssl_verify=ssl_verify)

    ssl_security_level = os.getenv("SSL_SECURITY_LEVEL", litellm.ssl_security_level)
    ssl_ecdh_curve = os.getenv("SSL_ECDH_CURVE", litellm.ssl_ecdh_curve)

    cafile = None
    if isinstance(ssl_verify, str) and os.path.exists(ssl_verify):
        cafile = ssl_verify
    if not cafile:
        ssl_cert_file = os.getenv("SSL_CERT_FILE")
        if ssl_cert_file and os.path.exists(ssl_cert_file):
            cafile = ssl_cert_file
        else:
            cafile = certifi.where()

    if ssl_verify is not False:
        # Create cache key from configuration parameters
        cache_key = (cafile, ssl_security_level, ssl_ecdh_curve)

        # Check if we have a cached SSL context for this configuration
        if cache_key not in _ssl_context_cache:
            _ssl_context_cache[cache_key] = _create_ssl_context(
                cafile=cafile,
                ssl_security_level=ssl_security_level,
                ssl_ecdh_curve=ssl_ecdh_curve,
            )

        # Return the cached SSL context
        return _ssl_context_cache[cache_key]

    return ssl_verify

