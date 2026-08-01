
def freeze_all(policies_per_player):
  """Freezes all policies within policy_per_player.

  Args:
    policies_per_player: List of list of number of policies.
  """
  for policies in policies_per_player:
    for pol in policies:
      pol.freeze()

