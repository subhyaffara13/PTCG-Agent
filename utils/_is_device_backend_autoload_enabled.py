
def _is_device_backend_autoload_enabled() -> builtins.bool:
    """
    Whether autoloading out-of-the-tree device extensions is enabled.
    The switch depends on the value of the environment variable
    `TORCH_DEVICE_BACKEND_AUTOLOAD`.

    Returns:
        bool: Whether to enable autoloading the extensions. Enabled by default.

    Examples:
        >>> torch._is_device_backend_autoload_enabled()
        True
    """
    # enabled by default
    return os.getenv("TORCH_DEVICE_BACKEND_AUTOLOAD", "1") == "1"

