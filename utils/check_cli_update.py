
def check_cli_update(library: Literal["huggingface_hub", "transformers"]) -> None:
    """
    Check whether a newer version of a library is available on PyPI.

    If a newer version is found, print a hint pointing at `hf update`.

    If current version is a pre-release (e.g. `1.0.0.rc1`), or a dev version (e.g. `1.0.0.dev1`), no check is performed.
    If `HF_HUB_DISABLE_UPDATE_CHECK` is set, the check is skipped entirely.

    This function is called at the entry point of the CLI. It only performs the check once every 24 hours, and any error
    during the check is caught and logged, to avoid breaking the CLI.

    Args:
        library: The library to check for updates. Currently supports "huggingface_hub" and "transformers".
    """
    try:
        _check_cli_update(library)
    except Exception:
        # We don't want the CLI to fail on version checks, no matter the reason.
        logger.debug("Error while checking for CLI update.", exc_info=True)

