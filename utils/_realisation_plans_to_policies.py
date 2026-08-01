
def _realisation_plans_to_policies(
    policies: list[policy.TabularPolicy],
    lps: list[lp_solver.LinearProgram],
    solutions: list[dict],
    infoset_action_maps: dict,
) -> None:
  """Conversion of a realisation plan to behavioural policies."""
  for pl_index in range(len(policies)):
    for info_state in infoset_action_maps[pl_index]:
      total_weight = 0
      num_actions = 0
      for isa_key in infoset_action_maps[pl_index][info_state]:
        total_weight += solutions[1 - pl_index][
            lps[1 - pl_index].get_var_id(isa_key)
        ]
        num_actions += 1
      unif_pr = 1.0 / num_actions
      state_policy = policies[pl_index].policy_for_key(info_state)
      for isa_key in infoset_action_maps[pl_index][info_state]:
        # The 1 - i here is due to Eq (8[1] or 2.4[2]) yielding a solution for
        # player 1 and Eq (9[1] or 2.5[2]) -- a solution for player 0.
        rel_weight = solutions[1 - pl_index][
            lps[1 - pl_index].get_var_id(isa_key)
        ]
        _, action_str = isa_key.split(_DELIMITER)
        action = int(action_str)
        pr_action = (
            rel_weight / total_weight if total_weight > 1e-20 else unif_pr
        )
        state_policy[action] = pr_action

