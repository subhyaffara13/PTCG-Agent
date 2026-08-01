
def _resolve_argnums(
    fun: tp.Callable,
    static_argnums: int | tp.Sequence[int] | None,
    static_argnames: str | tp.Iterable[str] | None,
) -> tuple[int, ...]:
  def _ensure_index_tuple(x: tp.Any) -> tuple[int, ...]:
    """Convert x to a tuple of indices."""
    try:
      return (operator.index(x),)
    except TypeError:
      return tuple(map(operator.index, x))

  def _ensure_str(x: str) -> str:
    if not isinstance(x, str):
      raise TypeError(f"argument is not a string: {x}")
    return x

  def _ensure_str_tuple(x: str | tp.Iterable[str]) -> tuple[str, ...]:
    """Convert x to a tuple of strings."""
    if isinstance(x, str):
      return (x,)
    else:
      return tuple(map(_ensure_str, x))

  signature = _fun_signature(fun)
  if signature is None:
    # Some built-in functions don't support signature.
    # See: https://github.com/python/cpython/issues/73485
    # In this case no validation is done
    static_argnums = () if static_argnums is None else _ensure_index_tuple(
        static_argnums)
  else:
    # Infer argnums and argnames according to docstring
    # If nums is None and names is not None, then nums are inferred from the
    # names and vice-versa.
    _POSITIONAL_OR_KEYWORD = inspect.Parameter.POSITIONAL_OR_KEYWORD
    _POSITIONAL_ARGUMENTS = (
      inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD
    )

    def infer_argnums_and_argnames(
        sig: inspect.Signature,
        argnums: int | tp.Iterable[int] | None,
        argnames: str | tp.Iterable[str] | None,
      ) -> tuple[tuple[int, ...], tuple[str, ...]]:
      """Infer missing argnums and argnames for a function with inspect."""
      if argnums is None and argnames is None:
        return (), ()

      if argnums is not None and argnames is not None:
        argnums = _ensure_index_tuple(argnums)
        argnames = _ensure_str_tuple(argnames)
        return argnums, argnames

      parameters = sig.parameters
      if argnums is None:
        assert argnames is not None
        argnames = _ensure_str_tuple(argnames)
        argnums = tuple(
            i for i, (k, param) in enumerate(parameters.items())
            if param.kind == _POSITIONAL_OR_KEYWORD and k in argnames
        )
      else:
        argnums = _ensure_index_tuple(argnums)
        argnames = tuple(
            k for i, (k, param) in enumerate(parameters.items())
            if param.kind == _POSITIONAL_OR_KEYWORD and i in argnums
        )
      return argnums, argnames

    def _validate_argnums(sig: inspect.Signature, argnums: tuple[int, ...], argnums_name: str) -> None:
      n_pos_args = 0
      for param in sig.parameters.values():
        if param.kind in _POSITIONAL_ARGUMENTS:
          n_pos_args += 1

        elif param.kind is inspect.Parameter.VAR_POSITIONAL:
          # We can have any number of positional arguments
          return

      if argnums and (-min(argnums) > n_pos_args or max(argnums) >= n_pos_args):
        raise ValueError(f"Jitted function has {argnums_name}={argnums}, "
                        f"but only accepts {n_pos_args} positional arguments.")

    static_argnums, static_argnames = infer_argnums_and_argnames(
        signature, static_argnums, static_argnames)

    # Validation
    _validate_argnums(signature, static_argnums, "static_argnums")

  return static_argnums

