
def _get_workload_cert_and_key(
    certificate_config_path=None, include_context_aware=True
):
    """Read the workload identity cert and key files specified in the certificate config provided.
    If no config path is provided, check the environment variable: "GOOGLE_API_CERTIFICATE_CONFIG"
    first, then the well known gcloud location: "~/.config/gcloud/certificate_config.json".

    Args:
        certificate_config_path (string): The certificate config path. If no path is provided,
        the environment variable will be checked first, then the well known gcloud location.
        include_context_aware (bool): If context aware metadata path should be checked for the
        SecureConnect mTLS configuration.

    Returns:
        Tuple[Optional[bytes], Optional[bytes]]: client certificate bytes in PEM format and key
            bytes in PEM format.

    Raises:
        google.auth.exceptions.ClientCertError: if problems occurs when retrieving
        the certificate or key information.
    """

    cert_path, key_path = _get_workload_cert_and_key_paths(
        certificate_config_path, include_context_aware
    )

    if cert_path is None and key_path is None:
        return None, None

    return _read_cert_and_key_files(cert_path, key_path)

