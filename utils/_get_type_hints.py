
def _get_type_hints(cls, *, include_extras: bool = False) -> _Hints:
  """`get_type_hints` with better error reporting."""
  # At this point, `ForwardRef` should have been resolved.
  try:
    return _get_type_hints_fix(cls, include_extras=include_extras)
  except Exception as e:  # pylint: disable=broad-except
    msg = (
        f'Could not infer typing annotation of {cls.__qualname__} '
        f'defined in {cls.__module__}:\n'
    )
    lines = [f' * {k}: {v!r}' for k, v in cls.__annotations__.items()]
    lines = '\n'.join(lines)

    epy.reraise(e, prefix=msg + lines + '\n')  # pytype: disable=bad-return-type

