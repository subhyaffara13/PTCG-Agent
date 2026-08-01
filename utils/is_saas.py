
def is_saas(host: str) -> bool:
    """Checks whether the connection is to the SaaS platform"""

    o = urlparse(host)

    if o.hostname and o.hostname.endswith("hiddenlayer.ai"):
        return True

    return False

