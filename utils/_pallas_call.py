from typing import Any, Callable

def _pallas_call(
    kernel: Callable[..., None],
    out_shape: Any,
    *,
    grid_spec: pallas_core.GridSpec,
    scratch_tree: tree_util.PyTreeDef,
    mesh: pallas_core.Mesh | None = None,
    input_output_aliases: Mapping[int, int] = {},
    debug: bool = False,
    interpret: Any = False,
    name: str | None = None,
    compiler_params: CompilerParams | None = None,
    cost_estimate: CostEstimate | None = None,
    metadata: dict[str, str] | None = None,
):
  interpret = (
      config.pallas_tpu_interpret_mode_context_manager.value or interpret)

  if mesh is not None:
    if tuple(mesh.shape.values()) != grid_spec.grid:
      raise ValueError(
          f"Mesh shape {tuple(mesh.shape.values())} does not match grid "
          f"shape {grid_spec.grid}."
      )

  grid_spec, dynamic_grid_bounds = pallas_core.unzip_dynamic_grid_bounds(grid_spec)
  # TODO(necula): this canonicalization may be convenient for some usage
  # but it is lossy, because it prevents expressing functions that return
  # lists.
  if isinstance(out_shape, list):
    out_shape = tuple(out_shape)
  flat_out_shapes_with_paths, out_tree = tree_util.tree_flatten_with_path(out_shape)
  out_paths, flat_out_shapes = unzip2(flat_out_shapes_with_paths)

  @api.jit(inline=True)
  def wrapped(*args):
    flat_args_with_paths, in_tree = tree_util.tree_flatten_with_path(args)
    in_paths, flat_args = unzip2(flat_args_with_paths)
    flat_in_avals = tuple(jax_core.typeof(a) for a in flat_args)

    flat_out_avals = tuple(
        pallas_core._convert_out_shape_to_aval(v) for v in flat_out_shapes
    )

    in_origins = tuple(f"args{tree_util.keystr(p)}" for p in in_paths)
    out_origins = tuple(f"outputs{tree_util.keystr(p)}" for p in out_paths)
    # TODO(necula): check that input_output_aliases is well-formed: no duplicates, etc.
    kernel_args, grid_mapping = pallas_core.get_grid_mapping(
        grid_spec,
        flat_in_avals,
        in_tree,
        in_origins,
        flat_out_avals,
        out_tree,
        out_origins,
        debug,
    )
    kernel_args, scratch_args = split_list(
        kernel_args, [len(kernel_args) - scratch_tree.num_leaves])
    scratch_args = scratch_tree.unflatten(scratch_args)
    if isinstance(scratch_args, dict):
      kernel_args_kwargs = (kernel_args, scratch_args)
    else:
      kernel_args_kwargs = (kernel_args + list(scratch_args), {})
    flat_kernel_args, kernel_in_tree = tree_util.tree_flatten(
        kernel_args_kwargs)
    flat_kernel_avals = tuple(
        x.ref if isinstance(x, state_types.TransformedRef) else x
        for x in flat_kernel_args
    )
    if config._check_vma.value:
      flat_kernel_avals = tuple(
        a.update_manual_axis_type(jax_core.empty_mat)
        for a in flat_kernel_avals
      )
    # Note that only a subset of all transforms can be found here, and they are
    # never expected to contain any arrays.
    kernel_arg_transforms = tuple(
        x.transforms if isinstance(x, state_types.TransformedRef) else ()
        for x in flat_kernel_args
    )
    kernel_dbg = api_util.debug_info("pallas_call kernel", kernel,
                                      *kernel_args_kwargs)
    if name is not None:
      kernel_dbg = kernel_dbg.replace_func_name(mlir.sanitize_name(name))
    jaxpr, consts = _trace_kernel_to_jaxpr(
        kernel, kernel_dbg, grid_mapping, flat_kernel_avals,
        kernel_in_tree, kernel_arg_transforms)
    for i_idx, o_idx in input_output_aliases.items():
      if i_idx not in range(len(flat_in_avals)):
        raise ValueError(
            f"input_output_aliases contains the mapping '{i_idx}:{o_idx}' with "
            f"input index {i_idx} outside the range "
            f"[0, {len(flat_in_avals)})")
      if o_idx not in range(len(flat_out_avals)):
        raise ValueError(
            f"input_output_aliases contains the mapping '{i_idx}:{o_idx}' with "
            f"output index {o_idx} outside the range "
            f"[0, {len(flat_out_avals)})")
      in_aval = flat_in_avals[i_idx]
      out_aval = flat_out_avals[o_idx]
      if in_aval.shape != out_aval.shape or in_aval.dtype != out_aval.dtype:  # pyrefly: ignore[missing-attribute]
        raise ValueError(
            f"input_output_aliases contains the mapping '{i_idx}:{o_idx}' "
            f"referring to input{tree_util.keystr(in_paths[i_idx])} with "
            f"abstract value {in_aval} "
            f"and to output{tree_util.keystr(out_paths[o_idx])} with "
            f"a different abstract value {out_aval}.")

    index_args, rest_args = split_list(flat_args, [grid_mapping.num_index_operands])
    ctx = (
        api.named_scope(name) if name is not None else contextlib.nullcontext()
    )
    with ctx:
      out_flat = pallas_call_p.bind(
          *consts,
          *dynamic_grid_bounds,
          *index_args,
          *rest_args,
          out_avals=flat_out_avals,
          jaxpr=jaxpr,
          debug=debug,
          interpret=interpret,
          grid_mapping=grid_mapping,
          mesh=mesh,
          input_output_aliases=tuple(input_output_aliases.items()),
          compiler_params=compiler_params,
          cost_estimate=cost_estimate,
          metadata=FrozenDict(metadata) if metadata is not None else None,
          name=name,
          # If we're running under GPU Interpret Mode, save the kernel arg
          # transforms. Checks the string name to avoid a conditional import.
          # TODO(jburnim): Clean this up.
          **(dict(kernel_arg_transforms=kernel_arg_transforms)
             if type(interpret).__name__ == "InterpretGPUParams" else {}),
      )
    out = tree_util.tree_unflatten(out_tree, out_flat)
    return out
  return wrapped

