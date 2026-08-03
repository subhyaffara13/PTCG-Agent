import os

def resolve_oci_credentials(optional_params: dict) -> dict:
    """
    Merge OCI credentials from optional_params (explicit, always wins) and
    environment variables (fallback).

    Returns a dict with resolved values for:
        oci_region, oci_user, oci_fingerprint, oci_tenancy,
        oci_key, oci_key_file, oci_compartment_id
    """
    return {
        "oci_region": optional_params.get("oci_region")
        or os.environ.get(_OCI_REGION_ENV)
        or "us-ashburn-1",
        "oci_user": optional_params.get("oci_user") or os.environ.get(_OCI_USER_ENV),
        "oci_fingerprint": optional_params.get("oci_fingerprint")
        or os.environ.get(_OCI_FINGERPRINT_ENV),
        "oci_tenancy": optional_params.get("oci_tenancy")
        or os.environ.get(_OCI_TENANCY_ENV),
        "oci_key": optional_params.get("oci_key") or os.environ.get(_OCI_KEY_ENV),
        "oci_key_file": optional_params.get("oci_key_file")
        or os.environ.get(_OCI_KEY_FILE_ENV),
        "oci_compartment_id": optional_params.get("oci_compartment_id")
        or os.environ.get(_OCI_COMPARTMENT_ID_ENV),
    }

