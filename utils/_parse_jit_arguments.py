from typing import Any, Callable

def _parse_jit_arguments(fun: Callable, *, in_shardings: Any,
                         out_shardings: Any,
                         static_argnums: int | Sequence[int] | None,
                         static_argnames: str | Iterable[str] | None,
                         donate_argnums: int | Sequence[int] | None,
                         donate_argnames: str | Iterable[str] | None,
                         keep_unused: bool, device: xc.Device | None,
                         backend: str | None, inline: bool,
                         compiler_options: dict[str, Any] | None,
                         use_resource_env: bool) -> PjitInfo:
  """Parses the arguments to jit/pjit.

  Performs any preprocessing and validation of the arguments that we can do
  ahead of time before the jit()-ed function is invoked.
  """
  check_callable(fun)

  if backend is not None or device is not None:
    warnings.warn(
        'backend and device argument on jit is deprecated. You can use'
        ' `jax.device_put(..., jax.local_devices(backend="cpu")[0])` on the'
        ' inputs to the jitted function to get the same behavior.',
        category=DeprecationWarning, stacklevel=5
    )
    if device is not None and backend is not None:
      raise ValueError("can't specify both a device and a backend for jit, "
                       f"got {device=} and {backend=}")
    if in_shardings is not None and not isinstance(in_shardings, UnspecifiedValue):
      raise ValueError('If backend or device is specified on jit, then '
                       'in_shardings should not be specified.')
    if out_shardings is not None and not isinstance(out_shardings, UnspecifiedValue):
      raise ValueError('If backend or device is specified on jit, then '
                       'out_shardings should not be specified.')

  if isinstance(in_shardings, list):
    # To be a tree prefix of the positional args tuple, in_axes can never be a
    # list: if in_axes is not a leaf, it must be a tuple of trees. However,
    # in cases like these users expect tuples and lists to be treated
    # essentially interchangeably, so we canonicalize lists to tuples here
    # rather than raising an error. https://github.com/jax-ml/jax/issues/2367
    in_shardings = tuple(in_shardings)

  in_layouts, in_shardings = _split_layout_and_sharding(in_shardings)
  out_layouts, out_shardings = _split_layout_and_sharding(out_shardings)

  in_shardings = prepare_axis_resources(in_shardings, 'in_shardings')
  out_shardings = prepare_axis_resources(out_shardings, 'out_shardings')

  user_specified_in_shardings = (in_shardings is not None and
                                 not isinstance(in_shardings, UnspecifiedValue))

  in_shardings_leaves, in_shardings_treedef = none_lr.flatten(in_shardings)
  out_shardings_leaves, out_shardings_treedef = none_lr.flatten(out_shardings)
  in_layouts_leaves, in_layouts_treedef = none_lr.flatten(in_layouts)
  out_layouts_leaves, out_layouts_treedef = none_lr.flatten(out_layouts)

  fun_sourceinfo = api_util.fun_sourceinfo(fun)
  fun_signature = api_util.fun_signature(fun)

  donate_argnums, donate_argnames, static_argnums, static_argnames = resolve_argnums(
      fun, fun_signature, donate_argnums, donate_argnames, static_argnums,
      static_argnames)

  compiler_options_kvs = (() if compiler_options is None else
                          tuple(compiler_options.items()))
  return PjitInfo(
        fun_sourceinfo=fun_sourceinfo,
        fun_signature=fun_signature,
        user_specified_in_shardings=user_specified_in_shardings,
        in_shardings_treedef=in_shardings_treedef,
        in_shardings_leaves=tuple(in_shardings_leaves),
        out_shardings_treedef=out_shardings_treedef,
        out_shardings_leaves=tuple(out_shardings_leaves),
        in_layouts_treedef=in_layouts_treedef,
        in_layouts_leaves=tuple(in_layouts_leaves),
        out_layouts_treedef=out_layouts_treedef,
        out_layouts_leaves=tuple(out_layouts_leaves),
        static_argnums=static_argnums,
        static_argnames=static_argnames, donate_argnums=donate_argnums,
        donate_argnames=donate_argnames, device=device, backend=backend,
        keep_unused=keep_unused, inline=inline,
        use_resource_env=use_resource_env,
        compiler_options_kvs=compiler_options_kvs)

