
def warn_experimental_arg_usage(
    arg_name: Union[list, str],
    function_name: str,
    stacklevel: int = 2,
):
    import warnings

    msg = (
        f"Call to '{function_name}' method with experimental"
        f" usage of input argument/s '{arg_name}'."
    )
    warnings.warn(msg, category=UserWarning, stacklevel=stacklevel)

