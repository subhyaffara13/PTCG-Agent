
def update_episodes_per_oracles(episodes_per_oracle, played_policies_indexes):
  """Updates the current episode count per policy.

  Args:
    episodes_per_oracle: List of list of number of episodes played per policy.
      One list per player.
    played_policies_indexes: List with structure (player_index, policy_index) of
      played policies whose count needs updating.

  Returns:
    Updated count.
  """
  for player_index, policy_index in played_policies_indexes:
    episodes_per_oracle[player_index][policy_index] += 1
  return episodes_per_oracle

