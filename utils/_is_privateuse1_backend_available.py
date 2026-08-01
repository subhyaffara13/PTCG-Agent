
def _is_privateuse1_backend_available():
    """
    Determines whether the privateuse1 backend is registered and available.

    Returns:
        Return True if the privateuse1 backend is registered and available.
    """
    privateuse1_backend_name = torch._C._get_privateuse1_backend_name()
    privateuse1_backend_module = getattr(torch, privateuse1_backend_name, None)
    return (
        is_available := getattr(privateuse1_backend_module, "is_available", None)
    ) and is_available()

