
def _non_static_arg_names(fn_signature: inspect.Signature | None,
                          args: Sequence[Any], kwargs: dict[str, Any],
                          static_argnums: Sequence[int],
                          static_argnames: Sequence[str],
                          ) -> tuple[str, ...]:
  """Returns the names of the non-static arguments.

  If the `fn_signature` is given then we get from it the names of the
  top-level arguments. In other cases, including when the `args` and `kwargs`
  do not match the signature, we use names like `args[0]`, `args[1]`, etc.
  """
  # Use the same argument parsing as jit: positional followed by kwargs
  # sorted by keys.
  static = object()
  static_argnums_ = _ensure_inbounds(True, len(args), static_argnums)
  static_argnames_ = set(static_argnames)
  args_ = [static if i in static_argnums_ else x for i, x in enumerate(args)]
  kwargs_ = {k: static if k in static_argnames_ else x for k, x in kwargs.items()}
  ordered_args: Sequence[tuple[str, Any]] | None = None
  if fn_signature is not None:
    try:
      ba = fn_signature.bind(*args_, **kwargs_)
    except (ValueError, TypeError):
      pass
    else:
      # Do we have a **kwargs
      kwargs_name = next((name for name, p in fn_signature.parameters.items()
                          if p.kind == inspect.Parameter.VAR_KEYWORD), None)
      # Positional argument are those not passed by keyword and not passed
      # by **kwargs.
      positional = [(name, x) for name, x in ba.arguments.items()
                    if name not in kwargs and name != kwargs_name]
      # Keyword arguments are passed sorted by actual kwarg keyword
      sorted_kwargs = sorted(((name, x) for name, x in kwargs_.items()),
                              key=lambda name_x: name_x[0])
      sorted_kwargs = [(name if name in ba.arguments else f"{kwargs_name}['{name}']",
                        x)
                       for name, x in sorted_kwargs]
      ordered_args = positional + sorted_kwargs

  if ordered_args is None:
    positional = [("args", args_)]
    keyword = sorted([(f"kwargs['{name}']", x) for name, x in kwargs_.items() if x is not static],
                     key=lambda name_x: name_x[0])
    ordered_args = positional + keyword

  return tuple(f'{name}{lu._clean_keystr_arg_names(path)}'
               for name, x in ordered_args
               for path, l in tracing_registry.flatten_with_path(x)[0]
               if l is not static)

