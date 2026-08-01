
def _apply_regret_matching_plus_reset(
    info_state_nodes: Dict[str, _InfoStateNode],
):
  """Resets negative cumulative regrets to 0.

  Regret Matching+ corresponds to the following cumulative regrets update:
  cumulative_regrets = max(cumulative_regrets + regrets, 0)

  This must be done at the level of the information set, and thus cannot be
  done during the tree traversal (which is done on histories). It is thus
  performed as an additional step.

  This function is a module level function to be reused by both CFRSolver and
  CFRBRSolver.

  Args:
    info_state_nodes: A dictionary {`info_state_str` -> `_InfoStateNode`}.
  """
  for info_state_node in info_state_nodes.values():
    action_to_cum_regret = info_state_node.cumulative_regret
    for action, cumulative_regret in action_to_cum_regret.items():
      if cumulative_regret < 0:
        action_to_cum_regret[action] = 0

