import json
from typing import Dict, Optional, Tuple

def sign_with_manual_credentials(
    headers: dict,
    optional_params: dict,
    request_data: dict,
    api_base: str,
) -> Tuple[dict, bytes]:
    """Sign a request using manually provided OCI credentials (user/fingerprint/tenancy/key)."""
    creds = resolve_oci_credentials(optional_params)
    oci_user = creds["oci_user"]
    oci_fingerprint = creds["oci_fingerprint"]
    oci_tenancy = creds["oci_tenancy"]
    oci_key = creds["oci_key"]
    oci_key_file = creds["oci_key_file"]

    if (
        not oci_user
        or not oci_fingerprint
        or not oci_tenancy
        or not (oci_key or oci_key_file)
    ):
        raise OCIError(
            status_code=401,
            message=(
                "Missing required OCI credentials: oci_user, oci_fingerprint, oci_tenancy, "
                "and at least one of oci_key or oci_key_file. "
                "These can also be supplied via environment variables: "
                f"{_OCI_USER_ENV}, {_OCI_FINGERPRINT_ENV}, {_OCI_TENANCY_ENV}, {_OCI_KEY_ENV} (or {_OCI_KEY_FILE_ENV}). "
                "Alternatively, provide an oci_signer object from the OCI SDK."
            ),
        )

    method = str(optional_params.get("method", "POST")).upper()
    body = json.dumps(request_data).encode("utf-8")
    parsed = urlparse(api_base)
    path = parsed.path or "/"
    host = parsed.netloc

    date = formatdate(usegmt=True)
    content_type = headers.get("content-type", "application/json")
    content_length = str(len(body))
    x_content_sha256 = sha256_base64(body)

    headers_to_sign: Dict[str, str] = {
        "date": date,
        "host": host,
        "content-type": content_type,
        "content-length": content_length,
        "x-content-sha256": x_content_sha256,
    }

    signed_header_names = [
        "date",
        "(request-target)",
        "host",
        "content-length",
        "content-type",
        "x-content-sha256",
    ]
    signing_string = build_signature_string(
        method, path, headers_to_sign, signed_header_names
    )

    _require_cryptography()

    # Resolve the private key — prefer inline PEM content over file path
    oci_key_content: Optional[str] = None
    if oci_key:
        if not isinstance(oci_key, str):
            raise OCIError(
                status_code=400,
                message=(
                    f"oci_key must be a string containing the PEM private key content. "
                    f"Got type: {type(oci_key).__name__}"
                ),
            )
        oci_key_content = oci_key.replace("\\n", "\n").replace("\r\n", "\n")

    private_key = (
        load_private_key_from_str(oci_key_content)
        if oci_key_content
        else load_private_key_from_file(oci_key_file) if oci_key_file else None
    )

    if private_key is None:
        raise OCIError(
            status_code=400,
            message="Private key is required for OCI authentication. Provide either oci_key or oci_key_file.",
        )

    signature = private_key.sign(
        signing_string.encode("utf-8"),
        padding.PKCS1v15(),  # type: ignore[union-attr]
        hashes.SHA256(),  # type: ignore[union-attr]
    )
    signature_b64 = base64.b64encode(signature).decode()

    key_id = f"{oci_tenancy}/{oci_user}/{oci_fingerprint}"
    authorization = (
        'Signature version="1",'
        f'keyId="{key_id}",'
        'algorithm="rsa-sha256",'
        f'headers="{" ".join(signed_header_names)}",'
        f'signature="{signature_b64}"'
    )

    headers.update(
        {
            "authorization": authorization,
            "date": date,
            "host": host,
            "content-type": content_type,
            "content-length": content_length,
            "x-content-sha256": x_content_sha256,
        }
    )
    return headers, body

