
def save_from_both_policies(policy_1, policy_2):
  """Logical OR of the given policies.

  A residual is saveable iff it is saveable according to either policy."""
  def policy(prim, *args, **params):
    out1 = policy_1(prim, *args, **params)
    out2 = policy_2(prim, *args, **params)
    if not (isinstance(out1, bool) and isinstance(out2, bool)):
      raise ValueError(
          "The return value of the policies should be a boolean. Got:"
          f" {out1} and {out2}. Please write a custom policy function directly,"
          " rather than using this helper function.")
    return out1 or out2
  return policy

