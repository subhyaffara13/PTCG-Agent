
def sign_with_oci_signer(
    headers: dict,
    optional_params: dict,
    request_data: dict,
    api_base: str,
) -> Tuple[dict, bytes]:
    """Sign a request using an OCI SDK Signer object passed in optional_params."""
    oci_signer = optional_params.get("oci_signer")
    body = json.dumps(request_data).encode("utf-8")
    method = str(optional_params.get("method", "POST")).upper()

    if method not in {"POST", "GET", "PUT", "DELETE", "PATCH"}:
        raise ValueError(f"Unsupported HTTP method: {method}")

    prepared_headers = {**headers}
    prepared_headers.setdefault("content-type", "application/json")
    prepared_headers.setdefault("content-length", str(len(body)))

    request_wrapper = OCIRequestWrapper(
        method=method, url=api_base, headers=prepared_headers, body=body
    )

    if oci_signer is None:
        raise ValueError("oci_signer cannot be None when calling sign_with_oci_signer")

    try:
        oci_signer.do_request_sign(request_wrapper, enforce_content_headers=True)
    except Exception as e:
        raise OCIError(
            status_code=500,
            message=(
                f"Failed to sign request with provided oci_signer: {str(e)}. "
                "The signer must implement the OCI SDK Signer interface with a "
                "do_request_sign(request, enforce_content_headers=True) method. "
                "See: https://docs.oracle.com/en-us/iaas/tools/python/latest/api/signing.html"
            ),
        ) from e

    headers.update(request_wrapper.headers)
    return headers, body

