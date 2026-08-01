
def _sdy_rule_for_aval(letters, num_batch_dims, aval):
  d = len(aval.shape) - num_batch_dims
  prefix = "... " if num_batch_dims and d >= 0 else ""
  return prefix + " ".join(next(letters) for _ in range(d))

