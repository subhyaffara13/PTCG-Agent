
def get_class_if_classified_error(e: Exception) -> str | None:
    """
    Returns a string case name if the export error e is classified.
    Returns None otherwise.
    """

    from torch._dynamo.exc import TorchRuntimeError, Unsupported, UserError

    ALWAYS_CLASSIFIED = "always_classified"
    DEFAULT_CLASS_SIGIL = "case_name"

    # add error types that should be classified, along with any attribute name
    # whose presence acts like a sigil to further distinguish which errors of
    # that type should be classified. If the attribute name is None, then the
    # error type is always classified.
    _ALLOW_LIST = {
        Unsupported: DEFAULT_CLASS_SIGIL,
        UserError: DEFAULT_CLASS_SIGIL,
        TorchRuntimeError: None,
    }
    if type(e) in _ALLOW_LIST:
        # pyrefly: ignore [bad-index, index-error]
        attr_name = _ALLOW_LIST[type(e)]
        if attr_name is None:
            return ALWAYS_CLASSIFIED
        return getattr(e, attr_name, None)
    return None

