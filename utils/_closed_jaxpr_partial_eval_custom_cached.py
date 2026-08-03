from typing import Callable

def _closed_jaxpr_partial_eval_custom_cached(
    jaxpr: ClosedJaxpr, unks_in: tuple[bool, ...], inst_in: tuple[bool, ...],
    disallowed_input_forwards: tuple[bool, ...],
    disallowed_output_forwards: tuple[bool, ...],
    saveable: Callable
    ) -> tuple[ClosedJaxpr, ClosedJaxpr, Sequence[bool], Sequence[bool],
               int, int, Sequence[int | None], Sequence[int | None]]:
  jaxpr_known_, jaxpr_staged_, unks_out, inst_out, num_res_val, num_res_ref = \
      partial_eval_jaxpr_stateful(jaxpr.jaxpr, unks_in, inst_in,
                                  False, False, saveable)

  num_out_primals = len(jaxpr_known_.outvars) - num_res_val
  out_vars, res_vars = split_list(jaxpr_known_.outvars, [num_out_primals])

  # Compute which residual value outputs are also primal inputs.
  disallowed, _ = partition_list(unks_in, disallowed_input_forwards)
  idx_map = {id(v): i for i, (v, b) in enumerate(zip(jaxpr_known_.invars, disallowed))
             if not b}
  in_fwd = [idx_map.get(id(v)) for v in res_vars]

  # Compute which residual value outputs are also *undropped* primal outputs.
  disallowed, _ = partition_list(unks_out, disallowed_output_forwards)
  idx_map = {id(v): i for i, (v, b) in enumerate(zip(out_vars, disallowed))
             if not b}
  out_fwd = [idx_map.get(id(v)) for v in res_vars]

  # Prune jaxpr_known_ outputs by removing forwards.
  keep = [f1 is f2 is None for f1, f2 in zip(in_fwd, out_fwd)]
  jaxpr_known_ = prune_jaxpr_outputs(jaxpr_known_, [True] * num_out_primals + keep)

  jaxpr_known = ClosedJaxpr(jaxpr_known_, jaxpr.consts)
  jaxpr_staged = ClosedJaxpr(jaxpr_staged_, jaxpr.consts)
  return jaxpr_known, jaxpr_staged, unks_out, inst_out, num_res_ref, num_res_val, in_fwd, out_fwd

