
def core_map(
    mesh,
    *,
    compiler_params: Any | None = None,
    interpret: bool = False,
    debug: bool = False,
    cost_estimate: CostEstimate | None = None,
    name: str | None = None,
    metadata: dict[str, str] | None = None,
    scratch_shapes: ScratchShapeTree = (),
):
  """Runs a function on a mesh, mapping it over the devices in the mesh.

  The function should be stateful in that it takes in no inputs and returns
  no outputs but can mutate closed-over Refs, for example.

  Args:
    mesh: The mesh to run the function on.
    compiler_params: The compiler parameters to pass to the backend.
    interpret: Whether to run the function in interpret mode.
    debug: Whether or not to out helpful debugging information.
    cost_estimate: The cost estimate of the function.
    name: The (optional) name of the kernel.
    metadata: Optional dictionary of information about the kernel that will be
      serialized as JSON in the HLO. Can be used for debugging and analysis.
    scratch_shapes: The scratch arrays for the kernel. Supports both sequence
      and dict format. The space will be core-local unless the memory space type
      is specified to be shared (e.g., VMEM_SHARED).
  """
  interpret = (
      config.pallas_tpu_interpret_mode_context_manager.value or interpret)

  def wrapped(f):
    if isinstance(scratch_shapes, dict):
      fun_args = ((), scratch_shapes)
    else:
      fun_args = (scratch_shapes, {})

    flat_args, in_tree = tree_util.tree_flatten(fun_args)
    debug_info = api_util.debug_info("pallas_core_map", f, *fun_args)  # pyrefly: ignore[bad-argument-type]
    flat_fun, out_tree_thunk = api_util.flatten_fun(
        lu.wrap_init(f, debug_info=debug_info), in_tree
    )
    ref_avals = tuple(t.get_ref_aval() for t in flat_args)
    with (
        tracing_grid_env(tuple(mesh.shape.values()), mapped_dims=()),
        jax_core.extend_axis_env_nd(mesh.shape.items()),
        config._check_vma(False),
    ):
      jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(flat_fun, ref_avals)

    out_tree = out_tree_thunk()
    if out_tree != tree_util.tree_structure(None):
      raise ValueError(
          f"The kernel function in core_map {debug_info.func_src_info} should"
          f" return None. It returns a PyTree: {out_tree}."
      )
    if debug:
      print(f"core_map jaxpr: {jaxpr}")

    out = core_map_p.bind(
        *consts,
        jaxpr=jaxpr,
        debug_info=debug_info,
        mesh=mesh,
        compiler_params=compiler_params,
        interpret=(
            config.pallas_tpu_interpret_mode_context_manager.value or interpret
        ),
        debug=debug,
        cost_estimate=cost_estimate,
        name=name or util.fun_name(f),
        metadata=frozen_dict.FrozenDict(metadata)
        if metadata is not None
        else None,
    )
    return tree_util.tree_unflatten(out_tree, out)

  return wrapped

