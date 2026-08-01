
def filter_policies(policies, new_policies, all_states):
  all_policies = policies
  no_novelty = True
  for new_policy in new_policies:
    if all([
        not equal_policies(new_policy, policy, all_states)
        for policy in all_policies
    ]):
      all_policies.append(new_policy)
      no_novelty = False
  return all_policies, no_novelty

