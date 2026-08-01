
def _configure_library_root_logger() -> None:
    global _default_handler

    with _lock:
        if _default_handler:
            # This library has already configured the library root logger.
            return
        _default_handler = logging.StreamHandler()  # Set sys.stderr as stream.
        # set defaults based on https://github.com/pyinstaller/pyinstaller/issues/7334#issuecomment-1357447176
        if sys.stderr is None:
            sys.stderr = open(os.devnull, "w")

        _default_handler.flush = sys.stderr.flush

        # Apply our default configuration to the library root logger.
        library_root_logger = _get_library_root_logger()
        library_root_logger.addHandler(_default_handler)
        library_root_logger.setLevel(_get_default_logging_level())
        # Always show lib when logging in non-verbose mode. Note, other libs
        # use `transformers.logger` directly, so we check `lib_name` to be safe
        lib_name = _get_library_name()
        logging_format = f"[{lib_name}] %(message)s"

        # if logging level is debug, we add pathname and lineno to formatter for easy debugging
        if os.getenv("TRANSFORMERS_VERBOSITY", None) == "detail":
            logging_format = "%(levelname)s [%(name)s:%(lineno)s] %(asctime)s %(message)s"

        formatter = logging.Formatter(logging_format)
        _default_handler.setFormatter(formatter)

        ci = os.getenv("CI")
        is_ci = ci is not None and ci.upper() in {"1", "ON", "YES", "TRUE"}
        library_root_logger.propagate = is_ci


def _configure_library_root_logger() -> None:
    library_root_logger = _get_library_root_logger()
    library_root_logger.addHandler(logging.StreamHandler())
    library_root_logger.setLevel(_get_default_logging_level())

