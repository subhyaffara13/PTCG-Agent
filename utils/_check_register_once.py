
def _check_register_once(module, attr) -> None:
    if hasattr(module, attr):
        raise RuntimeError(
            f"The custom device module of {module} has already been registered with {attr}"
        )

