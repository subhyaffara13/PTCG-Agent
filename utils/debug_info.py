
def debug_info(
    traced_for: str,
    fun: Callable,
    args: Sequence[Any],
    kwargs: dict[str, Any],
    *,
    static_argnums: Sequence[int] = (),
    static_argnames: Sequence[str] = (),
    result_paths_thunk: Callable[[], tuple[str, ...]] | core.InitialResultPaths = core.initial_result_paths,
    # TODO(necula): check if we really need this, e.g., to speed up tracing?
    sourceinfo: str | None = None,
    signature: inspect.Signature | None = None,
) -> core.DebugInfo:
  """Construct core.DebugInfo for a function given example args and kwargs.

  `args` and `kwargs` are example positional and keyword arguments, used with
  `inspect.Signature` to get the names of arguments. The arguments that are
  considered static for tracing purposes should be included, and designated
  using `static_argnums` and `static_argnames`.

  See docstring for linear_util.DebugInfo.
  """
  res = getattr(fun, "__fun_debug_info__", None)
  if res is not None:
    return res
  if sourceinfo is None:
    sourceinfo = fun_sourceinfo(fun)
  if signature is None:
    signature = fun_signature(fun)
  arg_names = _non_static_arg_names(signature, args, kwargs, static_argnums,
                                    static_argnames)
  return core.DebugInfo(traced_for, sourceinfo, arg_names, result_paths_thunk)

