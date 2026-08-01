
def remove_handler(handler: logging.Handler) -> None:
    """removes given handler from the HuggingFace Transformers's root logger."""

    _configure_library_root_logger()

    assert handler is not None and handler in _get_library_root_logger().handlers
    _get_library_root_logger().removeHandler(handler)


def remove_handler(key, handler):
    """
    Removes a handler from the ask system.

    .. deprecated:: 1.8.
        Use multipledispatch handler instead. See :obj:`~.Predicate`.

    """
    sympy_deprecation_warning(
        """
        The AskHandler system is deprecated. The remove_handler() function
        should be replaced with the multipledispatch handler of Predicate.
        """,
        deprecated_since_version="1.8",
        active_deprecations_target='deprecated-askhandler',
    )
    if isinstance(key, Predicate):
        key = key.name.name
    # Don't show the same warning again recursively
    with ignore_warnings(SymPyDeprecationWarning):
        getattr(Q, key).remove_handler(handler)

