from typing import Any

def _dedup_consts_and_unify_jaxpr_signatures(
    jaxprs: Sequence[jax_core.Jaxpr],
    consts_per_fn: Sequence[Sequence[Any]],
    flat_args: Sequence[Any],
    unflat_in_avals: Sequence[jax_core.AbstractValue],
    unflat_out_avals: Sequence[jax_core.AbstractValue],
    flat_kernel_avals: Sequence[jax_core.AbstractValue],
    meshes: Sequence[pallas_core.Mesh],
    all_meshes: tuple[pallas_core.Mesh, ...],
) -> tuple[list[jax_core.Jaxpr], list[Array]]:
  # Example:
  #   c1, c2, c3 are closed-over refs.
  #   fn1 closes over [c1, c2] -> traced jaxpr1 has constvars for [c1, c2]
  #   fn2 closes over [c2, c3] -> traced jaxpr2 has constvars for [c2, c3]
  #
  #   `_dedup_consts_and_unify_jaxpr_signatures` will:
  #     1. Deduplicate constants to `unique_consts` = [c1, c2, c3].
  #     2. Rewrite jaxprs to take all `unique_consts` as explicit inputs instead
  #        of constvars:
  #        new_jaxpr1: (in_args, c1, c2, c3, out_args, scratch_args) -> ()
  #        new_jaxpr2: (in_args, c1, c2, c3, out_args, scratch_args) -> ()
  #     3. Return the new jaxprs (with empty constvars) and `unique_consts`.

  unique_consts, const_ids = _get_unique_consts(consts_per_fn)

  arg_ids = {id(arg) for arg in flat_args}
  if any(const_id in arg_ids for const_id in const_ids):
    raise NotImplementedError(
        "Closed-over ref aliases with a passed-in ref is not supported."
    )

  unique_const_avals = [jax_core.typeof(c) for c in unique_consts]

  num_inputs = len(tree_util.tree_leaves(unflat_in_avals))
  num_outputs = len(tree_util.tree_leaves(unflat_out_avals))

  in_avals_flat, out_avals_flat, scratch_avals_flat = util.split_list(
      flat_kernel_avals, [num_inputs, num_outputs]
  )

  def make_rewritten_body(original_jaxpr, original_consts):
    def _rewritten_body(*args):
      in_args, unique_const_args, out_args, scratch_args = util.split_list(
          args, [num_inputs, len(unique_consts), num_outputs]
      )

      # Extract only the consts used by this jaxpr.
      c_map = {id(uc): arg for uc, arg in zip(unique_consts, unique_const_args)}
      mapped_consts = [c_map[id(c)] for c in original_consts]

      eval_args = in_args + out_args + scratch_args
      jax_core.eval_jaxpr(original_jaxpr, mapped_consts, *eval_args)
      return []

    return _rewritten_body

  new_jaxprs = []
  tracing_avals = (
      in_avals_flat + unique_const_avals + out_avals_flat + scratch_avals_flat
  )
  for mesh, jaxpr, consts in zip(meshes, jaxprs, consts_per_fn):
    debug_info = api_util.debug_info(
        "mpmd_map_closed_over",
        make_rewritten_body(jaxpr, consts),
        tracing_avals,
        {},
    )
    wrapped_fun = lu.wrap_init(
        make_rewritten_body(jaxpr, consts), debug_info=debug_info
    )
    with mpmd_map_tracing_context(mesh, all_meshes):
      new_jaxpr, _, new_consts = pe.trace_to_jaxpr_dynamic(
          wrapped_fun, tracing_avals
      )
    assert not new_consts
    new_jaxprs.append(new_jaxpr)
  return new_jaxprs, unique_consts

