
def load_module_from_name(dotted_name: str) -> types.ModuleType:
    """Load a Python module from its name.

    :type dotted_name: str
    :param dotted_name: python name of a module or package

    :raise ImportError: if the module or package is not found

    :rtype: module
    :return: the loaded module
    """
    try:
        return sys.modules[dotted_name]
    except KeyError:
        pass

    # Capture and log anything emitted during import to avoid
    # contaminating JSON reports in pylint
    with (
        redirect_stderr(io.StringIO()) as stderr,
        redirect_stdout(io.StringIO()) as stdout,
    ):
        module = importlib.import_module(dotted_name)

    stderr_value = stderr.getvalue()
    if stderr_value:
        logger.error(
            "Captured stderr while importing %s:\n%s", dotted_name, stderr_value
        )
    stdout_value = stdout.getvalue()
    if stdout_value:
        logger.info(
            "Captured stdout while importing %s:\n%s", dotted_name, stdout_value
        )

    return module

