
def validate_bnb_backend_availability(raise_exception=False):
    """
    Validates if the available devices are supported by bitsandbytes, optionally raising an exception if not.
    """
    bnb_supported_devices = getattr(bnb, "supported_torch_devices", set())
    available_devices = set(get_available_devices())

    if not available_devices.intersection(bnb_supported_devices):
        if raise_exception:
            err_msg = (
                f"None of the available devices `available_devices = {available_devices or None}` are supported by the bitsandbytes version you have installed: `bnb_supported_devices = {bnb_supported_devices}`. "
                "Please check the docs to see if the backend you intend to use is available and how to install it: https://huggingface.co/docs/bitsandbytes/main/en/installation"
            )
            raise RuntimeError(err_msg)

        logger.warning("No supported devices found for bitsandbytes")
        return False
    return True

