
def get_client_ssl_credentials(
    generate_encrypted_key=False,
    context_aware_metadata_path=CONTEXT_AWARE_METADATA_PATH,
    certificate_config_path=None,
):
    """Returns the client side certificate, private key and passphrase.

    We look for certificates and keys with the following order of priority:
        1. Certificate and key specified by certificate_config.json.
               Currently, only X.509 workload certificates are supported.
        2. Certificate and key specified by context aware metadata (i.e. SecureConnect).

    Args:
        generate_encrypted_key (bool): If set to True, encrypted private key
            and passphrase will be generated; otherwise, unencrypted private key
            will be generated and passphrase will be None. This option only
            affects keys obtained via context_aware_metadata.json.
        context_aware_metadata_path (str): The context_aware_metadata.json file path.
        certificate_config_path (str): The certificate_config.json file path.

    Returns:
        Tuple[bool, bytes, bytes, bytes]:
            A boolean indicating if cert, key and passphrase are obtained, the
            cert bytes and key bytes both in PEM format, and passphrase bytes.

    Raises:
        google.auth.exceptions.ClientCertError: if problems occurs when getting
            the cert, key and passphrase.
    """

    # 1.  Attempt to retrieve X.509 Workload cert and key.
    cert, key = _get_workload_cert_and_key(certificate_config_path)
    if cert and key:
        return True, cert, key, None

    # 2. Check for context aware metadata json
    metadata_path = _check_config_path(context_aware_metadata_path)

    if metadata_path:
        metadata_json = _load_json_file(metadata_path)

        if _CERT_PROVIDER_COMMAND not in metadata_json:
            raise exceptions.ClientCertError("Cert provider command is not found")

        command = metadata_json[_CERT_PROVIDER_COMMAND]

        if generate_encrypted_key and "--with_passphrase" not in command:
            command.append("--with_passphrase")

        # Execute the command.
        cert, key, passphrase = _run_cert_provider_command(
            command, expect_encrypted_key=generate_encrypted_key
        )
        return True, cert, key, passphrase

    return False, None, None, None

