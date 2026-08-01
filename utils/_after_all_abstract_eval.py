
def _after_all_abstract_eval(*operands):
  if any(x is not abstract_token for x in operands):
    raise TypeError("Arguments to after_all must be tokens")
  return abstract_token

