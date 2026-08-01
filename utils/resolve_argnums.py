
def resolve_argnums(
    fun: Callable,
    signature: inspect.Signature | None,
    donate_argnums: int | Sequence[int] | None,
    donate_argnames: str | Iterable[str] | None,
    static_argnums: int | Sequence[int] | None,
    static_argnames: str | Iterable[str] | None,
) -> tuple[tuple[int, ...], tuple[str, ...], tuple[int, ...], tuple[str, ...]]:
  """Validates and completes the argnum/argname specification for a jit.

  * fills in any missing pieces (e.g., names given numbers, or vice versa),
  * validates the argument names/numbers against the function signature,
  * validates that donated and static arguments don't intersect.
  """
  if signature is None:
    # Some built-in functions don't support signature.
    # See: https://github.com/python/cpython/issues/73485
    # In this case no validation is done
    static_argnums = () if static_argnums is None else _ensure_index_tuple(
        static_argnums)
    static_argnames = () if static_argnames is None else _ensure_str_tuple(
        static_argnames)
    donate_argnums = () if donate_argnums is None else _ensure_index_tuple(
        donate_argnums)
    if donate_argnames is not None:
      raise ValueError(f"Getting the signature of function {fun} failed. "
                       "Pass donate_argnums instead of donate_argnames.")
    assert donate_argnames is None
    donate_argnames = ()
  else:
    # Infer argnums and argnames according to docstring
    # If nums is None and names is not None, then nums are inferred from the
    # names and vice-versa.
    static_argnums, static_argnames = infer_argnums_and_argnames(
        signature, static_argnums, static_argnames)
    donate_argnums, donate_argnames = infer_argnums_and_argnames(
        signature, donate_argnums, donate_argnames)

    # Validation
    _validate_argnums(signature, static_argnums, "static_argnums")
    _validate_argnames(signature, static_argnames, "static_argnames")
    _validate_argnums(signature, donate_argnums, "donate_argnums")
    _validate_argnames(signature, donate_argnames, "donate_argnames")

  # Compensate for static argnums absorbing args
  _assert_no_intersection(static_argnames, donate_argnames)
  return donate_argnums, donate_argnames, static_argnums, static_argnames

