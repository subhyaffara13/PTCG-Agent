
def expand_in_shardings(in_shardings: Sequence[LoweringSharding],
                        module_kept_var_idx: Sequence[int],
                        nr_inputs: int) -> Sequence[LoweringSharding]:
  """Expands in_shardings with unspecified shardings for inputs not kept.

  Assumes in_shardings corresponds to module_kept_var_idx.
  """
  assert len(in_shardings) == len(module_kept_var_idx)
  assert nr_inputs >= len(module_kept_var_idx)
  all_in_shardings: list[LoweringSharding] = [sharding_impls.UNSPECIFIED] * nr_inputs
  for idx, in_s in zip(sorted(module_kept_var_idx), in_shardings):
    all_in_shardings[idx] = in_s
  return tuple(all_in_shardings)

