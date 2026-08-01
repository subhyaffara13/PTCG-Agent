
def print_verbose(print_statement):
    try:
        verbose_logger.debug(print_statement)
        if litellm.set_verbose:
            print(print_statement)  # noqa: T201
    except Exception:
        pass


def print_verbose(
    print_statement,
    logger_only: bool = False,
    log_level: Literal["DEBUG", "INFO", "ERROR"] = "DEBUG",
):
    try:
        if log_level == "DEBUG":
            verbose_logger.debug(print_statement)
        elif log_level == "INFO":
            verbose_logger.info(print_statement)
        elif log_level == "ERROR":
            verbose_logger.error(print_statement)
        if litellm.set_verbose is True and logger_only is False:
            print(print_statement)  # noqa: T201
    except Exception:
        pass


def print_verbose(print_statement):
    try:
        if set_verbose:
            print(redact_secrets(str(print_statement)))  # noqa: T201
    except Exception:
        pass


def print_verbose(print_statement):
    try:
        verbose_logger.debug(print_statement)
        if litellm.set_verbose:
            print(print_statement)  # noqa: T201
    except Exception:
        pass


def print_verbose(print_statement):
    try:
        if litellm.set_verbose:
            print(print_statement)  # noqa: T201
    except Exception:
        pass


def print_verbose(print_statement):
    """
    Prints the given `print_statement` to the console if `litellm.set_verbose` is True.
    Also logs the `print_statement` at the debug level using `verbose_proxy_logger`.

    :param print_statement: The statement to be printed and logged.
    :type print_statement: Any
    """
    import traceback

    verbose_proxy_logger.debug("{}\n{}".format(print_statement, traceback.format_exc()))
    if litellm.set_verbose:
        print(f"LiteLLM Proxy: {_redact_string(str(print_statement))}")  # noqa: T201


def print_verbose(print_statement):
    if litellm.set_verbose:
        print(print_statement)  # noqa

