from typing import Optional, Tuple

def sign_oci_request(
    headers: dict,
    optional_params: dict,
    request_data: dict,
    api_base: str,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    stream: Optional[bool] = None,
    fake_stream: Optional[bool] = None,
) -> Tuple[dict, bytes]:
    """
    Route to the appropriate OCI signing method based on what credentials are present.

    If ``oci_signer`` is in optional_params, use the OCI SDK signer object.
    Otherwise use manual RSA-SHA256 signing with explicit credentials (which can
    also be supplied via OCI_* environment variables).

    Returns:
        Tuple of (signed_headers, signed_body_bytes)
    """
    if optional_params.get("oci_signer") is not None:
        return sign_with_oci_signer(headers, optional_params, request_data, api_base)
    return sign_with_manual_credentials(
        headers, optional_params, request_data, api_base
    )

