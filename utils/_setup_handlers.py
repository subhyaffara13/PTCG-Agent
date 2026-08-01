
def _setup_handlers(create_handler_fn, log) -> None:
    debug_handler = _track_handler(create_handler_fn())
    debug_handler.setFormatter(DEFAULT_FORMATTER)
    debug_handler.setLevel(logging.DEBUG)
    log.addHandler(debug_handler)

