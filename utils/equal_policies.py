
def equal_policies(pol1, pol2, all_states):
  assert isinstance(pol1, greedy_policy.GreedyPolicy)
  equal = True
  for state_key in all_states:
    state = all_states[state_key]
    try:
      equal = equal and dict_equal(pol1(state), pol2(state))
    except KeyError:
      equal = False
    except ValueError:
      continue
  return equal

