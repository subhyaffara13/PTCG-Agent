
def register_handler(handler: ImageFile.StubHandler | None) -> None:
    """
    Install application-specific BUFR image handler.

    :param handler: Handler object.
    """
    global _handler
    _handler = handler


def register_handler(handler: ImageFile.StubHandler | None) -> None:
    """
    Install application-specific GRIB image handler.

    :param handler: Handler object.
    """
    global _handler
    _handler = handler


def register_handler(handler: ImageFile.StubHandler | None) -> None:
    """
    Install application-specific HDF5 image handler.

    :param handler: Handler object.
    """
    global _handler
    _handler = handler


def register_handler(handler: ImageFile.StubHandler | None) -> None:
    """
    Install application-specific WMF image handler.

    :param handler: Handler object.
    """
    global _handler
    _handler = handler


def register_handler(key, handler):
    """
    Register a handler in the ask system. key must be a string and handler a
    class inheriting from AskHandler.

    .. deprecated:: 1.8.
        Use multipledispatch handler instead. See :obj:`~.Predicate`.

    """
    sympy_deprecation_warning(
        """
        The AskHandler system is deprecated. The register_handler() function
        should be replaced with the multipledispatch handler of Predicate.
        """,
        deprecated_since_version="1.8",
        active_deprecations_target='deprecated-askhandler',
    )
    if isinstance(key, Predicate):
        key = key.name.name
    Qkey = getattr(Q, key, None)
    if Qkey is not None:
        Qkey.add_handler(handler)
    else:
        setattr(Q, key, Predicate(key, handlers=[handler]))


def register_handler(
    cls: CheckpointableHandlerType,
    *,
    checkpointable_name: str | None = None,
    secondary_typestrs: Sequence[str] | None = None,
) -> CheckpointableHandlerType:
  """Registers a :py:class:`~.v1.handlers.CheckpointableHandler` globally.

  The order in which handlers are registered strictly matters. If multiple
  handlers could potentially be used to save or load an object (i.e., are
  capable of handling the checkpointable according to `is_handleable`/
  `is_abstract_handleable` for `save`/`load`, respectively), the framework
  resolves them in Last-In, First-Out (LIFO) order. This means the handler
  added most recently will be selected.

  Example:
    Registering a custom handler using a direct function call.
    Note the import path from the v1 namespace::

      from orbax.checkpoint.v1 import handlers

      class BarHandler(handlers.CheckpointableHandler):
        pass

      handlers.register_handler(BarHandler)

  Args:
    cls: The handler class to register globally.
    checkpointable_name: The checkpointable name. If not-None, the registered
      handler will be scoped to that specific name. Otherwise, the handler
      will be available for any checkpointable name.
    secondary_typestrs: A sequence of alternate handler typestrs that serve as
      secondary identifiers for the handler.

  Returns:
    The handler class.
  """
  _GLOBAL_REGISTRY.add(
      cls,
      checkpointable_name=checkpointable_name,
      secondary_typestrs=secondary_typestrs,
  )
  return cls

