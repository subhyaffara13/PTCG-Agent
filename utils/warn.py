
def warn(
    msg: str,
    *args: object,
    category: Optional[Type[Warning]] = None,
    stacklevel: int = 1,
):
    """Raises a warning to the user if the min_level <= WARN.

    Args:
        msg: The message to warn the user
        *args: Additional information to warn the user
        category: The category of warning
        stacklevel: The stack level to raise to
    """
    if min_level <= WARN:
        warnings.warn(
            colorize(f"WARN: {msg % args}", "yellow"),
            category=category,
            stacklevel=stacklevel + 1,
        )


def warn(
    msg: str,
    *args: object,
    category: type[Warning] | None = None,
    stacklevel: int = 1,
):
    """Raises a warning to the user if the min_level <= WARN.

    Args:
        msg: The message to warn the user
        *args: Additional information to warn the user
        category: The category of warning
        stacklevel: The stack level to raise to
    """
    if min_level <= WARN:
        warnings.warn(
            colorize(f"WARN: {msg % args}", "yellow"),
            category=category,
            stacklevel=stacklevel + 1,
        )


def warn(msg: str, category: t.Any, *, stacklevel: int, source: t.Any = None) -> None:
    """Like warnings.warn(), but category and stacklevel are required.

    You pretty much never want the default stacklevel of 1, so this helps
    encourage setting it explicitly."""
    warnings.warn(msg, category=category, stacklevel=stacklevel, source=source)


def warn(deprecation_id: str, message: str, stacklevel: int, *,
         error_class: type[Exception] = ValueError) -> None:
  """Warns about a deprecation, or errors if the deprecation is accelerated."""
  if is_accelerated(deprecation_id):
    assert issubclass(error_class, Exception)
    raise error_class(message)
  else:
    warnings.warn(message, category=DeprecationWarning,
                  stacklevel=stacklevel + 1)


def warn(msg, *args, **kwargs):
  """Deprecated, use 'warning' instead."""
  warnings.warn("The 'warn' function is deprecated, use 'warning' instead",
                DeprecationWarning, 2)
  log(WARNING, msg, *args, **kwargs)

