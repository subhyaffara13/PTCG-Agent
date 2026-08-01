
def capture_logging() -> Generator[StringIO, None, None]:
    """Capture all pip logs in a buffer temporarily."""
    # Patching sys.std(out|err) directly is not viable as the caller
    # may want to emit non-logging output (e.g. a rich spinner). To
    # avoid capturing that, temporarily patch the root logging handlers
    # to use new rich consoles that write to a StringIO.
    handlers = {}
    for handler in logging.getLogger().handlers:
        if isinstance(handler, RichPipStreamHandler):
            # Also store the handler's original console so it can be
            # restored on context exit.
            handlers[handler] = handler.console

    fake_stream = StreamWrapper.from_stream(sys.stdout)
    if not handlers:
        yield fake_stream
        return

    # HACK: grab no_color attribute from a random handler console since
    # it's a global option anyway.
    no_color = next(iter(handlers.values())).no_color
    fake_console = PipConsole(file=fake_stream, no_color=no_color, soft_wrap=True)
    try:
        for handler in handlers:
            handler.console = fake_console
        yield fake_stream
    finally:
        for handler, original_console in handlers.items():
            handler.console = original_console

