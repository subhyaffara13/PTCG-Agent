
def check_if_dynamo_supported() -> None:
    if sys.version_info >= (3, 15):
        raise RuntimeError("Python 3.15+ not yet supported for torch.compile")
    elif sysconfig.get_config_var("Py_GIL_DISABLED") == 1 and sys.version_info < (
        3,
        13,
        3,
    ):
        raise RuntimeError(
            "torch.compile is not supported on Python < 3.13.3 built with GIL disabled. "
            "Please use Python 3.13.3+."
        )

