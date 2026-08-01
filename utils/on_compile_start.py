
def on_compile_start(
    callback: Callable[[CallbackArgs], None],
) -> Callable[[CallbackArgs], None]:
    """
    Decorator to register a callback function for the start of the compilation.
    """
    callback_handler.register_start_callback(callback)
    return callback

