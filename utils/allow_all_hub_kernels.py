
def allow_all_hub_kernels():
    """
    Context manager used to adjust the value of the global `ALLOW_HUB_KERNELS`. This is needed, as this argument
    cannot be forwarded directly to the `__init__` of the models, where we set the attention implementation.
    """
    global ALLOW_ALL_KERNELS

    try:
        ALLOW_ALL_KERNELS = True

        yield
    finally:
        # Set back the original
        ALLOW_ALL_KERNELS = False

