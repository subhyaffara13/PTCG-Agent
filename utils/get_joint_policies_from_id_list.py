
def get_joint_policies_from_id_list(payoff_tables, policies, profile_id_list):
  """Returns a list of joint policies, given a list of integer IDs.

  Args:
    payoff_tables: List of payoff tables, one per player.
    policies: A list of policies, one per player.
    profile_id_list: list of integer IDs, each corresponding to a joint policy.
      These integers correspond to those in get_strategy_profile_ids().

  Returns:
    selected_joint_policies: A list, with each element being a joint policy
      instance (i.e., a list of policies, one per player).
  """
  num_strats_per_population = (
      alpharank_utils.get_num_strats_per_population(
          payoff_tables, payoffs_are_hpt_format=False))
  np.testing.assert_array_equal(num_strats_per_population,
                                [len(p) for p in policies])
  num_players = len(policies)

  selected_joint_policies = []
  for profile_id in profile_id_list:
    # Compute the profile associated with the integer profile_id
    policy_profile = alpharank_utils.get_strat_profile_from_id(
        num_strats_per_population, profile_id)
    # Append the joint policy corresponding to policy_profile
    selected_joint_policies.append(
        [policies[k][policy_profile[k]] for k in range(num_players)])
  return selected_joint_policies

