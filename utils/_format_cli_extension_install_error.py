
def _format_cli_extension_install_error(error: CLIExtensionInstallError) -> str:
    """Format a CLI extension installation error.

    The error is likely to be a tricky subprocess error to investigate. In this specific case we want to format the
    traceback of the root cause while keeping the "nicely formatted" error message of the CLIExtensionInstallError
    as a 1-line message.
    """
    cause_tb = (
        "".join(traceback.format_exception(type(error.__cause__), error.__cause__, error.__cause__.__traceback__))
        if error.__cause__ is not None
        else ""
    )
    return f"{cause_tb}\n{error}"

