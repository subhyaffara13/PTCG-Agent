
def _import_device_backends():
    """
    Leverage the Python plugin mechanism to load out-of-the-tree device extensions.
    See this RFC: https://github.com/pytorch/pytorch/issues/122468
    """
    from importlib.metadata import entry_points

    group_name = "torch.backends"
    backend_extensions = entry_points(group=group_name)

    for backend_extension in backend_extensions:
        try:
            # Load the extension
            entrypoint = backend_extension.load()
            # Call the entrypoint
            entrypoint()
        except Exception as err:
            raise RuntimeError(
                f"Failed to load the backend extension: {backend_extension.name}. "
                f"You can disable extension auto-loading with TORCH_DEVICE_BACKEND_AUTOLOAD=0."
            ) from err

