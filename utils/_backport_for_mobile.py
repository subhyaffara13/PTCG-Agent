
def _backport_for_mobile(f_input, f_output, to_version):
    r"""Take a input string containing a file name (file-like object) and a new destination to return a boolean.

    Args:
        f_input: a file-like object (has to implement read, readline, tell, and seek),
            or a string containing a file name
        f_output: path to new model destination
        to_version: the expected output model bytecode version
    Returns:
        success: A boolean. If backport success, return true, otherwise false
    """
    if isinstance(f_input, (str, os.PathLike)):
        if not os.path.exists(f_input):
            raise ValueError(f"The provided filename {f_input} does not exist")
        if os.path.isdir(f_input):
            raise ValueError(f"The provided filename {f_input} is a directory")

    if (isinstance(f_input, (str, os.PathLike))) and (
        isinstance(f_output, (str, os.PathLike))
    ):
        return torch._C._backport_for_mobile(
            os.fspath(f_input),
            os.fspath(f_output),
            to_version,
        )
    else:
        return torch._C._backport_for_mobile_from_buffer(
            f_input.read(),
            str(f_output),
            to_version,
        )

