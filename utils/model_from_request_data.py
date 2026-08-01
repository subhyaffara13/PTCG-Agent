
def model_from_request_data(data: object) -> str | None:
    """The user-facing ``model`` from a pre-call ``data`` dict (``None`` if absent).

    Read at the auth boundary to label early Baggage before routing has resolved
    a deployment; ``data`` is duck-typed since it arrives untyped from the proxy.
    """
    if isinstance(data, Mapping):
        return as_str(data.get("model"))
    return None

