
def _recognized_hosts(endpoint: str | None) -> frozenset[str]:
    """The set of hosts whose web URLs can be parsed: the default Hugging Face hosts plus 'endpoint'."""
    host, _ = _endpoint_host_and_path(endpoint)
    return constants.HF_URL_HOSTS | {host} if host else constants.HF_URL_HOSTS

