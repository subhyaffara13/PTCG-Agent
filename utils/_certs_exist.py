import os

def _certs_exist(mds_mtls_config: MdsMtlsConfig):
    """Checks if the mTLS certificates exist."""
    return os.path.exists(mds_mtls_config.ca_cert_path) and os.path.exists(
        mds_mtls_config.client_combined_cert_path
    )

