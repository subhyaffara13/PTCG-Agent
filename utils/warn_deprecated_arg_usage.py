from typing import Union

def warn_deprecated_arg_usage(
    arg_name: Union[list, str],
    function_name: str,
    reason: str = "",
    version: str = "",
    stacklevel: int = 2,
):
    import warnings

    msg = (
        f"Call to '{function_name}' function with deprecated"
        f" usage of input argument/s '{arg_name}'."
    )
    if reason:
        msg += f" ({reason})"
    if version:
        msg += f" -- Deprecated since version {version}."
    warnings.warn(msg, category=DeprecationWarning, stacklevel=stacklevel)

