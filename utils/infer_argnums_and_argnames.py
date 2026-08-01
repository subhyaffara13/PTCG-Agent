
def infer_argnums_and_argnames(
    sig: inspect.Signature,
    argnums: int | Iterable[int] | None,
    argnames: str | Iterable[str] | None,
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

