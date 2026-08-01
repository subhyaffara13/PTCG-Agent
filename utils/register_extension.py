
def register_extension(id: str, extension: str) -> None:
    """
    Registers an image extension.  This function should not be
    used in application code.

    :param id: An image format identifier.
    :param extension: An extension used for this format.
    """
    EXTENSION[extension.lower()] = id.upper()


def register_extension(
    op_type: type[Any],
    extension_handler: type[ExtensionHandler],
):
    """Register custom de/serialization method for a node with non-standard type."""
    if not issubclass(extension_handler, ExtensionHandler):
        raise AssertionError(f"Expected ExtensionHandler, got {extension_handler}.")
    if op_type in _serialization_registry:
        raise AssertionError(f"{op_type} is already registered.")
    if not isinstance(op_type, type):
        raise AssertionError(f"op_type must be a type, got {type(op_type).__name__}")
    if op_type.__module__.startswith("torch") or op_type.__module__.startswith(
        "builtins"
    ):
        raise AssertionError(
            f"op_type module {op_type.__module__} should not start with 'torch' or 'builtins'"
        )
    if extension_handler.namespace() in _deserialization_registry:
        raise AssertionError(
            f"namespace {extension_handler.namespace()!r} is already registered"
        )
    _serialization_registry[op_type] = extension_handler
    _deserialization_registry[extension_handler.namespace()] = extension_handler

