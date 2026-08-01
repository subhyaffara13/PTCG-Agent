
def get_agent_identity_certificate_path():
    """Gets the certificate path from the certificate config file.

    The path to the certificate config file is read from the
    GOOGLE_API_CERTIFICATE_CONFIG environment variable. This function
    implements a retry mechanism to handle cases where the environment
    variable is set before the files are available on the filesystem.

    Returns:
        str: The path to the leaf certificate file.

    Raises:
        google.auth.exceptions.RefreshError: If the certificate config file
            or the certificate file cannot be found after retries.
    """
    import json

    cert_config_path = os.environ.get(environment_vars.GOOGLE_API_CERTIFICATE_CONFIG)

    # Check if the well-known workload directory is mounted.
    well_known_dir = os.path.dirname(_WELL_KNOWN_CERT_PATH)
    has_well_known_dir = os.path.exists(well_known_dir)

    # If we have neither a config path nor a well-known mount directory, exit immediately.
    if not cert_config_path and not has_well_known_dir:
        return None

    # If ECP config path is specified but does not exist, and we are on a workstation, fail-fast immediately.
    if (
        cert_config_path
        and not has_well_known_dir
        and not os.path.exists(cert_config_path)
    ):
        return None

    has_logged_config_warning = False
    has_logged_cert_warning = False

    for interval in _POLLING_INTERVALS:
        try:
            # Path A: Config file is explicitly set
            if cert_config_path:
                with open(cert_config_path, "r") as f:
                    cert_config = json.load(f)

                cert_configs = (
                    cert_config.get("cert_configs")
                    if isinstance(cert_config, dict)
                    else None
                )
                workload_config = (
                    cert_configs.get("workload")
                    if isinstance(cert_configs, dict)
                    else None
                )

                if (
                    not isinstance(workload_config, dict)
                    or "cert_path" not in workload_config
                ):
                    return None

                cert_path = workload_config["cert_path"]
                if _is_certificate_file_ready(cert_path):
                    return cert_path

                # The config was parsed, but the cert file is not ready yet
                target_path = cert_path

            # Path B: Config is NOT set, fallback to the well-known path
            else:
                if _is_certificate_file_ready(_WELL_KNOWN_CERT_PATH):
                    return _WELL_KNOWN_CERT_PATH

                # The well-known cert file is not ready yet
                target_path = _WELL_KNOWN_CERT_PATH

            # Log a warning on the first failed attempt to load the certificate file
            if not has_logged_cert_warning:
                _LOGGER.warning(
                    "Certificate file not ready at %s. Retrying until startup timeout (up to %s seconds total)...",
                    target_path,
                    _TOTAL_TIMEOUT,
                )
                has_logged_cert_warning = True

        except (IOError, ValueError, KeyError) as e:
            if cert_config_path and os.path.exists(cert_config_path):
                # If the file exists but has invalid JSON or is unreadable,
                # we assume it is in its final format and fail-fast by returning None.
                return None

            if not has_logged_config_warning and cert_config_path:
                _LOGGER.warning(
                    "Certificate config file not found or incomplete: %s (from %s "
                    "environment variable). Retrying until startup timeout (up to %s seconds total)...",
                    e,
                    environment_vars.GOOGLE_API_CERTIFICATE_CONFIG,
                    _TOTAL_TIMEOUT,
                )
                has_logged_config_warning = True
            pass

        # A sleep is required in two cases:
        # 1. The config file is not found (the except block).
        # 2. The config file/well-known path is found, but the certificate is not yet available.
        # In both cases, we need to poll, so we sleep on every iteration
        # that doesn't return a certificate.
        time.sleep(interval)

    raise exceptions.RefreshError(
        "Certificate config or certificate file not found after multiple retries. "
        f"Token binding protection is failing. You can turn off this protection by setting "
        f"{environment_vars.GOOGLE_API_PREVENT_AGENT_TOKEN_SHARING_FOR_GCP_SERVICES} to false "
        "to fall back to unbound tokens."
    )

