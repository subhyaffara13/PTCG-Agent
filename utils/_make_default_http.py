
def _make_default_http():
    if certifi is not None:
        return urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
    else:
        return urllib3.PoolManager()

