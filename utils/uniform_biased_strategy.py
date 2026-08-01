
def uniform_biased_strategy(solver, return_joint=False):
  """Returns a Biased Random Uniform distribution on policies.

  The uniform distribution is biased to prioritize playing against more recent
  policies (Policies that were appended to the policy list later in training)
  instead of older ones.

  Args:
    solver: GenPSROSolver instance.
    return_joint: If true, only returns marginals. Otherwise marginals as well
      as joint probabilities.

  Returns:
    uniform distribution on strategies.
  """
  policies = solver.get_policies()
  if not isinstance(policies[0], list):
    policies = [policies]
  policy_lengths = [len(pol) for pol in policies]
  result = [softmax_on_range(pol_len) for pol_len in policy_lengths]
  if not return_joint:
    return result
  else:
    joint_strategies = get_joint_strategy_from_marginals(result)
    return result, joint_strategies

