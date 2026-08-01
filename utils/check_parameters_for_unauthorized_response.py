
def check_parameters_for_unauthorized_response(cached_cert):
    """Returns the cached and current cert fingerprint for reconfiguring mTLS.

    Args:
        cached_cert(bytes): The cached client certificate.

    Returns:
        bytes: The client callback cert bytes.
        bytes: The client callback key bytes.
        str: The base64-encoded SHA256 cached fingerprint.
        str: The base64-encoded SHA256 current cert fingerprint.
    """
    call_cert_bytes, call_key_bytes = call_client_cert_callback()
    cert_obj = _agent_identity_utils.parse_certificate(call_cert_bytes)
    current_cert_fingerprint = _agent_identity_utils.calculate_certificate_fingerprint(
        cert_obj
    )
    if cached_cert:
        cached_fingerprint = _agent_identity_utils.get_cached_cert_fingerprint(
            cached_cert
        )
    else:
        cached_fingerprint = current_cert_fingerprint
    return call_cert_bytes, call_key_bytes, cached_fingerprint, current_cert_fingerprint

