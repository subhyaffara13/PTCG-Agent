
def _get_mds_root_crt_path():
    if os.name == _WINDOWS_OS_NAME:
        return _WINDOWS_MTLS_COMPONENTS_BASE_PATH / "mds-mtls-root.crt"
    else:
        return _MTLS_COMPONENTS_BASE_PATH / "root.crt"

