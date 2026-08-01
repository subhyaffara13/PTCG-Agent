
def requires_backends(obj, backends):
    """
    Method that automatically raises in case the specified backends are not available. It is often used during class
    initialization to ensure the required dependencies are installed:

    ```py
    requires_backends(self, ["torch"])
    ```

    The backends should be defined in the `BACKEND_MAPPING` defined in `transformers.utils.import_utils`.

    Args:
        obj: object to be checked
        backends: list or tuple of backends to check.
    """
    if not isinstance(backends, list | tuple):
        backends = [backends]

    name = obj.__name__ if hasattr(obj, "__name__") else obj.__class__.__name__

    failed = []
    for backend in backends:
        if isinstance(backend, Backend):
            available, msg = backend.is_satisfied, backend.error_message
        else:
            available, msg = BACKENDS_MAPPING[backend]

        if not available():
            failed.append(msg.format(name))

    if failed:
        raise ImportError("".join(failed))

