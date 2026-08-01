
def _compile_to_executable(
    name: str,
    fun: Callable[..., Any],
    in_specs_treedef: tree_util.PyTreeDef,
    in_specs_leaves: tuple[api.ShapeDtypeStruct, ...],
    out_specs_treedef: tree_util.PyTreeDef,
    out_specs_leaves: tuple[api.ShapeDtypeStruct, ...],
    devices: xc.DeviceList,
) -> Callable[..., Any]:
  """Compiles a Python function into a runtime executable."""
  # PRNG key dtypes are not supported by IFRT's colocated python programs.
  # Convert them to their physical representation for compilation, and
  # wrap/unwrap at the function boundary.
  prng_in_info = _get_prng_key_info(in_specs_leaves)
  prng_out_info = _get_prng_key_info(out_specs_leaves)
  in_specs_leaves = _convert_inp_type_to_physical(in_specs_leaves, prng_in_info)
  out_specs_leaves = _convert_inp_type_to_physical(out_specs_leaves, prng_out_info)

  # Wrap the user function to handle PRNG key conversion on the worker side.
  if prng_in_info or prng_out_info:
    fun = _make_prng_wrapped_fun(fun, prng_in_info, prng_out_info)

  fun_and_specialization = (
      fun,
      in_specs_treedef,
      in_specs_leaves,
      out_specs_treedef,
      out_specs_leaves,
      devices,
  )
  pickled_function = _serialize(fun_and_specialization)
  program = ifrt_programs.make_colocated_python_program(
      name, pickled_function, devices, in_specs_leaves, out_specs_leaves
  )
  ifrt_client = devices[0].client
  out_sdss = tuple(
      jax.core.ShapedArray(sds.shape, sds.dtype) for sds in out_specs_leaves
  )
  out_shardings = tuple(sds.sharding for sds in out_specs_leaves)
  try:
    compile_options = ifrt_programs.make_colocated_python_compile_options()
    loaded_executable = ifrt_client.compile_ifrt_program(
        program, compile_options
    )
    out_handlers = pxla.global_avals_to_results_handler(
        out_sdss, out_shardings, committed=True
    ).handlers

    def call(*args, **kwargs):
      args_leaves = tree_util.tree_leaves((args, kwargs))
      # Unwrap PRNG key inputs to physical before passing to IFRT.
      args_leaves = _unwrap_prng_keys(args_leaves, prng_in_info)
      execute_result = loaded_executable.execute_sharded(
          args_leaves, with_tokens=False
      )
      results = execute_result.consume_with_handlers(out_handlers)
      # Wrap physical outputs back to PRNG key arrays.
      results = _wrap_prng_keys(results, prng_out_info)
      return tree_util.tree_unflatten(out_specs_treedef, results)

    return call
  except jax.errors.JaxRuntimeError as e:
    # TODO(hyeontaek): Implement colocated Python support in McJAX and remove
    # this fallback path.
    if "PjRtCompiler requires an HloProgram" in str(e):
      deserialized_fun = _deserialize(pickled_function)[0]

      @wraps(deserialized_fun)
      def fallback_call(*args, __deserialized_fun=deserialized_fun, **kwargs):
        # Unwrap PRNG key inputs to physical before calling the user function.
        args_leaves, in_treedef = tree_util.tree_flatten((args, kwargs))
        args_leaves = _unwrap_prng_keys(args_leaves, prng_in_info)
        args, kwargs = tree_util.tree_unflatten(in_treedef, args_leaves)

        results = __deserialized_fun(*args, **kwargs)

        # Wrap physical outputs back to PRNG key arrays.
        results_leaves, out_treedef = tree_util.tree_flatten(results)
        results_leaves = _wrap_prng_keys(results_leaves, prng_out_info)
        return tree_util.tree_unflatten(out_treedef, results_leaves)

      return fallback_call
    raise

