
def _policy_dict_at_state(callable_policy, state):
  """Turns a policy function into a dictionary at a specific state.

  Args:
    callable_policy: A function from `state` -> lis of (action, prob),
    state: the specific state to extract the policy from.

  Returns:
    A dictionary of action -> prob at this state.
  """

  infostate_policy_list = callable_policy(state)
  infostate_policy = {}
  for ap in infostate_policy_list:
    infostate_policy[ap[0]] = ap[1]
  return infostate_policy

