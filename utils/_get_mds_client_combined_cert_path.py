
def _get_mds_client_combined_cert_path():
    if os.name == _WINDOWS_OS_NAME:
        return _WINDOWS_MTLS_COMPONENTS_BASE_PATH / "mds-mtls-client.key"
    else:
        return _MTLS_COMPONENTS_BASE_PATH / "client.key"

