
def _get_init_val_literal(op_type, is_max_k):
  return np.array(-np.inf if is_max_k else np.inf, dtype=op_type)

