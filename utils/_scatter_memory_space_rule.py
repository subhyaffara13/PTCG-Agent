
def _scatter_memory_space_rule(
    operand, indices, updates, *, update_jaxpr, update_consts,
    dimension_numbers, indices_are_sorted, unique_indices, mode):
  return operand.memory_space

