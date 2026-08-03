from typing import Optional

def get_oci_base_url(optional_params: dict, api_base: Optional[str] = None) -> str:
    """Return the OCI inference base URL, respecting any explicit api_base override.

    If ``api_base`` already ends with a fully-formed OCI action path
    (``/{OCI_API_VERSION}/actions/<name>``), that suffix is stripped so callers
    can append their own action path without producing a doubled URL.
    """
    if api_base:
        return _OCI_ACTION_PATH_RE.sub("", api_base).rstrip("/")
    creds = resolve_oci_credentials(optional_params)
    region = creds["oci_region"]
    if not isinstance(region, str) or not _OCI_REGION_RE.match(region):
        raise OCIError(
            status_code=400,
            message=(
                f"Invalid OCI region {region!r}: must match "
                "^[a-z][a-z0-9-]{0,30}[a-z0-9]$ (e.g. 'us-ashburn-1')."
            ),
        )
    return f"https://inference.generativeai.{region}.oci.oraclecloud.com"

