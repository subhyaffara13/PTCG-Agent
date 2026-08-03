import functools
from typing import Any, Callable

def _mpmd_map(
    meshes_and_fns: Sequence[tuple[pallas_core.Mesh, Callable[..., None]]],
    /,
    out_types: tree_util.PyTree = (),
    *,
    input_output_aliases: Mapping[int, int] = {},
    scratch_types: pallas_core.ScratchShapeTree = (),
    compiler_params: Any | None = None,
    interpret: bool | Any = False,
    debug: bool = False,
    cost_estimate: pallas_core.CostEstimate | None = None,
    name: str | None = None,
    metadata: dict[str, str] | None = None,
) -> Callable[..., _T]:
  """Like ``pallas_call``, but MPMD and without pipelining."""
  if not meshes_and_fns:
    raise ValueError("At least one mesh/function pair is required")

  is_output_sequence = isinstance(out_types, Sequence)

  flat_out_types_with_paths, out_tree = tree_util.tree_flatten_with_path(
      out_types
  )
  out_paths, flat_out_types = util.unzip2(flat_out_types_with_paths)
  # TODO(sharadmv): Use out_paths for debugging info.
  del out_paths
  flat_out_avals = tuple(
      map(pallas_core._convert_out_shape_to_aval, flat_out_types)
  )

  def wrapper(*args):
    flat_args_with_paths, in_tree = tree_util.tree_flatten_with_path(args)
    in_paths, flat_args = util.unzip2(flat_args_with_paths)
    del in_paths

    seen_ref_ids = set()
    for arg in flat_args:
      if isinstance(arg, jax_core.Ref):
        if id(arg) in seen_ref_ids:
          raise NotImplementedError(
              "Cannot pass the same ref into a mpmd map multiple times"
          )
        seen_ref_ids.add(id(arg))
    # TODO(sharadmv): Use in_paths for debugging info.
    flat_avals = tuple(map(jax_core.typeof, flat_args))

    external_meshes = []
    meshes = tuple(mesh for mesh, _ in meshes_and_fns)

    flat_scratch_types, scratch_tree = tree_util.tree_flatten(scratch_types)
    if len(meshes_and_fns) > 1:
      # TODO(rdyro): For MPMD with more than one mesh, come up with a better
      # solution for how to enforce core_type presence in scratch_shape.
      # TODO(rdyro): Check if we need to have a similar check for in-kernel
      # allocations (e.g., run_scoped, empty_ref) or can we assume the
      # core_type is inherited from the caller (we then need the core_type in
      # the caller context during tracing).
      # TODO(rdyro): Also check inputs and outputs for core type.
      for scratch_type in flat_scratch_types:
        from jax._src.pallas.mosaic import core as tpu_core  # pyrefly: ignore[missing-import]

        if not isinstance(
            scratch_type.memory_space, pallas_core.CoreMemorySpace
        ) and scratch_type.memory_space not in (
            tpu_core.MemorySpace.HBM,
            tpu_core.MemorySpace.VMEM_SHARED,
        ):
          raise NotImplementedError(
              "MPMD map with more than one mesh requires scratch_type to have"
              f" a `core_type` specified, but {scratch_type=} is missing it."
          )

    # Kernels may have Refs that belong to external meshes (usually for
    # async kernels). For example, the SC ScalarSubcore may have a Reference
    # to a TC semaphore that it is signaling. There is no explicit TC mesh as
    # part of the user-provided meshes, and are instead snuck in via the aval.
    for aval in [*flat_avals, *flat_out_avals, *flat_scratch_types]:
      if (
          isinstance(aval, jax_core.ShapedArray)
          and isinstance(aval.memory_space, pallas_core.CoreMemorySpace)
          and aval.memory_space.mesh not in it.chain(meshes, external_meshes)
      ):
        external_meshes.append(aval.memory_space.mesh)

    all_meshes = (*meshes, *external_meshes)
    # Check that meshes are compatible with each other (e.g, have a consistent
    # core axis name in the sparsecore).
    for i, mesh in enumerate(all_meshes):
      for other_mesh in list(all_meshes)[i + 1 :]:
        mesh.check_is_compatible_with(other_mesh)

    unflat_in_avals = in_tree.unflatten(flat_avals)
    unflat_out_avals = out_tree.unflatten(flat_out_avals)
    unflat_scratch_types = scratch_tree.unflatten(flat_scratch_types)
    kernel_arg_avals = list(unflat_in_avals)
    if is_output_sequence:
      kernel_arg_avals.extend(unflat_out_avals)
    else:
      kernel_arg_avals.append(unflat_out_avals)
    if isinstance(unflat_scratch_types, Mapping):
      kernel_kwarg_avals = unflat_scratch_types
    else:
      kernel_arg_avals.extend(unflat_scratch_types)
      kernel_kwarg_avals = {}

    unflat_kernel_avals = tree_util.tree_map(
        functools.partial(_aval_to_ref_aval, meshes=meshes),
        (kernel_arg_avals, kernel_kwarg_avals),
    )
    flat_kernel_avals, kernel_aval_tree = tree_util.tree_flatten(
        unflat_kernel_avals
    )

    jaxprs: list[jax_core.Jaxpr] = []
    consts_per_fn = []
    for mesh, fn in meshes_and_fns:
      debug_info = api_util.debug_info("mpmd_map", fn, flat_kernel_avals, {})
      if name is not None:
        debug_info = debug_info.replace_func_name(name)
      flat_fun, out_tree_thunk = api_util.flatten_fun(
          lu.wrap_init(fn, debug_info=debug_info), kernel_aval_tree
      )
      with mpmd_map_tracing_context(mesh, all_meshes):
        jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(
            flat_fun, flat_kernel_avals
        )
      fun_out_tree = out_tree_thunk()
      if fun_out_tree != tree_util.tree_structure(None):
        raise ValueError(
            f"The kernel function in mpmd_map {debug_info.func_src_info}"
            f" should return None. It returns a PyTree: {fun_out_tree}."
        )
      if consts:
        _error_if_non_ref_consts(consts, debug_info)
      jaxprs.append(jaxpr)
      consts_per_fn.append(consts)

    if any(consts_per_fn):
      # If we close over any constants in the kernel functions, we need to
      # deduplicate them and then unify the jaxpr signatures.
      jaxprs, consts = _dedup_consts_and_unify_jaxpr_signatures(
          jaxprs,
          consts_per_fn,
          flat_args,
          unflat_in_avals,
          unflat_out_avals,
          flat_kernel_avals,
          meshes,
          all_meshes,
      )
    else:
      consts: list[Array] = []

    if debug:
      for mesh, jaxpr in zip(meshes, jaxprs):
        print(f"jaxpr for {mesh.core_type}")
        print(jaxpr)

    # TODO(slebedev): The named scope should not be necessary here.
    ctx = (
        api.named_scope(name) if name is not None else contextlib.nullcontext()
    )
    with ctx:
      flat_outs = mpmd_map_p.bind(
          *flat_args,
          *consts,
          meshes=tuple(meshes),
          jaxprs=tuple(jaxprs),
          external_meshes=tuple(external_meshes),
          out_avals=flat_out_avals,
          input_output_aliases=FrozenDict(input_output_aliases),
          compiler_params=compiler_params,
          interpret=interpret,
          debug=debug,
          cost_estimate=cost_estimate,
          metadata=FrozenDict(metadata) if metadata is not None else None,
          name=name,
      )
    return out_tree.unflatten(flat_outs)

  return cast(Callable[..., _T], wrapper)

