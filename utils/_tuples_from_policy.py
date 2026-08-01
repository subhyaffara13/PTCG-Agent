
def _tuples_from_policy(policy_vector):
  return [
      (action, probability) for action, probability in enumerate(policy_vector)
  ]

