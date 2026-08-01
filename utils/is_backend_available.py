
def is_backend_available(backend: str) -> bool:
    """
    Check backend availability.

    Checks if the given backend is available and supports the built-in backends or
    third-party backends through function ``Backend.register_backend``.

    Args:
        backend (str): Backend name.
    Returns:
        bool: Returns true if the backend is available otherwise false.
    """
    # If the backend has an ``is_backend_available`` function, return the result of that function directly
    if ":" in backend.lower():  # composite backend like "cpu:gloo"
        backend_config = BackendConfig(Backend(backend))
        device_backend_map = backend_config.get_device_backend_map()
        return all(
            _check_single_backend_availability(str(backend_name))
            for backend_name in device_backend_map.values()
        )
    else:
        # Handle simple backend strings like "nccl", "gloo"
        return _check_single_backend_availability(backend)

