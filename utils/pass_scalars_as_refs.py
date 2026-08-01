
def pass_scalars_as_refs(
    jaxpr: jax_core.Jaxpr,
    args: Sequence[Any],
    in_avals: Sequence[jax_core.AbstractValue],
    out_avals: Sequence[jax_core.AbstractValue],
    mesh,
    copy_to_smem: bool = False,
) -> tuple[
    jax_core.Jaxpr,
    tuple[Any, ...],
    tuple[jax_core.AbstractValue, ...],
    tuple[jax_core.AbstractValue, ...],
    tuple[bool, ...],
]:
  """Rewrites a jaxpr to pass scalars as refs instead of values."""
  def allowed_aval(aval):
    if isinstance(aval, state.AbstractRef):
      return True
    if isinstance(aval, jax_core.ShapedArray):
      # Only scalars are allowed.
      return not aval.shape
    return False

  assert all(allowed_aval(v.aval) for v in jaxpr.constvars + jaxpr.invars)

  is_scalar_const = [
      isinstance(v.aval, jax_core.ShapedArray) and not v.aval.shape
      for v in jaxpr.constvars
  ]
  if not any(is_scalar_const):
    return (
        jaxpr,
        tuple(in_avals),
        tuple(out_avals),
        tuple(args),
        tuple(is_scalar_const),
    )
  non_scalar_const_avals, scalar_const_avals = util.partition_list(
      is_scalar_const,
      [v.aval for v in jaxpr.constvars],
  )
  non_scalar_consts, scalar_consts = util.partition_list(
      is_scalar_const, args
  )
  if copy_to_smem:
    smem_alloc = [
        state.AbstractRef(
            jax_core.ShapedArray((1,), aval.dtype),  # pyrefly: ignore[missing-attribute]
            memory_space=MemorySpace.SMEM,
        )
        for aval in scalar_const_avals
    ]
  else:
    smem_alloc = []

  # Rewrite body jaxpr to take in scalar values as Refs.
  def new_body(*args):
    scalar_const_refs, non_scalar_const_refs, args = util.split_list(
        args, [len(scalar_consts), len(non_scalar_consts)]
    )
    if copy_to_smem:
      smem, args = util.split_list(args, [len(smem_alloc)])
      assert len(smem) == len(scalar_const_refs)
      from jax._src.pallas.mosaic.helpers import sync_copy  # pyrefly: ignore[missing-import]

      sync_copy(scalar_const_refs, smem)
    else:
      smem = scalar_const_refs
    scalar_const_values = [s[0] for s in smem]
    new_consts = util.merge_lists(
        is_scalar_const, non_scalar_const_refs, scalar_const_values
    )
    return jax_core.eval_jaxpr(jaxpr, new_consts, *args)

  # TODO(sharadmv): Remove this once Mosaic support passing scalars as values.
  scalar_const_trace_avals = [
      state.AbstractRef(
          jax_core.ShapedArray((1,), aval.dtype),  # pyrefly: ignore[missing-attribute]
          memory_space=MemorySpace.HBM if copy_to_smem else MemorySpace.SMEM,
      )
      for aval in scalar_const_avals
  ]
  new_trace_avals = [
      *scalar_const_trace_avals,
      *non_scalar_const_avals,
      *smem_alloc,
      *[v.aval for v in jaxpr.invars],
  ]
  with (
      pallas_core.tracing_grid_env(
          tuple(mesh.shape.values()), mapped_dims=()
      ),
      jax_core.extend_axis_env_nd(mesh.shape.items()),
  ):
    new_jaxpr, _, _ = pe.trace_to_jaxpr_dynamic(
        lu.wrap_init(
            new_body, debug_info=jaxpr.debug_info.with_unknown_names()
        ),
        new_trace_avals,
    )
  jaxpr = new_jaxpr.replace(
      constvars=new_jaxpr.invars[: len(jaxpr.constvars)],
      invars=new_jaxpr.invars[len(jaxpr.constvars) :],
  )
  args = [
      *[a[None] for a in scalar_consts],
      *non_scalar_consts,
  ]
  in_avals, out_avals, _ = util.split_list(
      new_trace_avals, [len(in_avals), len(out_avals)]
  )
  return jaxpr, tuple(in_avals), tuple(out_avals), tuple(args), tuple(is_scalar_const)

