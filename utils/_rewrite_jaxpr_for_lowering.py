
def _rewrite_jaxpr_for_lowering(
    jaxpr: jax_core.Jaxpr,
    mesh: pallas_core.Mesh,
    all_meshes: tuple[pallas_core.Mesh, ...],
) -> jax_core.Jaxpr:
  # If the jaxpr has any scalar shaped arrays as inputs, they must have come
  # from closed over scalars. We need to rewrite the jaxpr to actually take in
  # a (1,) shaped Ref as an input. On TC and SC Vector Subcore, this Ref will be
  # in SMEM and on the SC scalar subcore, it will be in SMEM.
  core_type = mesh.core_type
  is_scalar_input = [
      isinstance(v.aval, jax_core.ShapedArray) and not v.aval.shape
      for v in jaxpr.invars
  ]
  if not any(is_scalar_input):
    return jaxpr

  new_in_avals = []
  for is_scalar, v in zip(is_scalar_input, jaxpr.invars):
    if not is_scalar:
      new_in_avals.append(v.aval)
      continue
    if core_type == tpu_core.CoreType.TC:
      # TC compiler supports passing Refs in SMEM directly.
      mem_space = tpu_core.MemorySpace.SMEM
    elif core_type in (
        tpu_core.CoreType.SC_SCALAR_SUBCORE,
        tpu_core.CoreType.SC_VECTOR_SUBCORE,
    ):
      # SC compiler doesn't support pass-via-SMEM so we need to pass the Refs
      # in HBM and then copy them into SMEM inside the kernel.
      mem_space = tpu_core.MemorySpace.HBM
    else:
      raise ValueError(f"Unsupported core type: {core_type}")
    new_in_avals.append(
        state.AbstractRef(
            jax_core.ShapedArray((1,), v.aval.dtype), memory_space=mem_space  # pyrefly: ignore[missing-attribute]
        )
    )

  def new_body(*args):
    sync_copy_srcs = []
    sync_copy_dsts = []
    refs = []
    # First pass: collect the destinations and sources for all scalar inputs
    # so we can perform a single, grouped sync_copy for performance.
    for is_scalar, arg in zip(is_scalar_input, args):
      if not is_scalar:
        refs.append(None)
        continue
      if core_type == tpu_core.CoreType.TC:
        refs.append(arg)
      elif core_type == tpu_core.CoreType.SC_SCALAR_SUBCORE:
        smem_ref = jax.empty_ref(
            jax_core.ShapedArray((1,), arg.dtype),
            memory_space=tpu_core.MemorySpace.SMEM,
        )
        sync_copy_srcs.append(arg)
        sync_copy_dsts.append(smem_ref)
        refs.append(smem_ref)
      elif core_type == tpu_core.CoreType.SC_VECTOR_SUBCORE:
        num_lanes = sc_core.get_sparse_core_info().num_lanes
        vmem_ref = jax.empty_ref(
            jax_core.ShapedArray((num_lanes,), arg.dtype),
            memory_space=tpu_core.MemorySpace.VMEM,
        )
        sync_copy_srcs.append(arg)
        sync_copy_dsts.append(vmem_ref.at[:1])
        refs.append(vmem_ref)

    # Perform bulk sync_copy for all scalars before any reads are emitted.
    if sync_copy_srcs:
      helpers.sync_copy(tuple(sync_copy_srcs), tuple(sync_copy_dsts))

    processed_args = []
    # Second pass: load values from the populated SMEM/VMEM references.
    # Doing this in a second pass ensures the read operations appear after
    # the sync_copy operation in the traced jaxpr.
    for is_scalar, arg, ref in zip(is_scalar_input, args, refs):
      if is_scalar:
        assert ref is not None
        if core_type == tpu_core.CoreType.SC_VECTOR_SUBCORE:
          processed_args.append(ref[...][0])
        else:
          processed_args.append(ref[0])
      else:
        processed_args.append(arg)

    return jax_core.eval_jaxpr(jaxpr, jaxpr.constvars, *processed_args)

  with mpmd.mpmd_map_tracing_context(mesh, all_meshes):
    new_jaxpr, _, new_consts = pe.trace_to_jaxpr_dynamic(
        lu.wrap_init(
            new_body, debug_info=jaxpr.debug_info.with_unknown_names()
        ),
        new_in_avals,
    )
  assert not new_consts
  return new_jaxpr

