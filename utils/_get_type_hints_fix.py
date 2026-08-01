
def _get_type_hints_fix(cls, *, include_extras: bool = False) -> _Hints:
  """`get_type_hints` with bug fixes."""
  # TODO(py311): `get_type_hints` fail for `_: dataclasses.KW_ONLY`
  old_annotations = [_fix_annotations(subcls) for subcls in cls.mro()]
  try:
    return typing_extensions.get_type_hints(cls, include_extras=include_extras)
  finally:
    # Restore the annotations
    for subcls, annotations in zip(cls.mro(), old_annotations):
      if annotations:
        subcls.__annotations__ = annotations

