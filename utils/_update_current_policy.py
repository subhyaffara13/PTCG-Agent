
def _update_current_policy(
    current_policy: policy.TabularPolicy,
    info_state_nodes: Dict[str, _InfoStateNode],
):
  """Updates in place `current_policy` from the cumulative regrets.

  This function is a module level function to be reused by both CFRSolver and
  CFRBRSolver.

  Args:
    current_policy: A `policy.TabularPolicy` to be updated in-place.
    info_state_nodes: A dictionary {`info_state_str` -> `_InfoStateNode`}.
  """
  for info_state, info_state_node in info_state_nodes.items():
    state_policy = current_policy.policy_for_key(info_state)

    for action, value in _regret_matching(
        info_state_node.cumulative_regret,
        info_state_node.legal_actions).items():
      state_policy[action] = value

