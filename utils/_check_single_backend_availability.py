
def _check_single_backend_availability(backend_name: str) -> bool:
    """
    Helper function to check if a single backend is available.
    """
    available_func = getattr(
        torch.distributed, f"is_{str(backend_name).lower()}_available", None
    )
    if available_func:
        return available_func()
    return str(backend_name).lower() in Backend.backend_list

