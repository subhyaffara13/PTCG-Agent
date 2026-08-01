
def print_policy_analysis(policies, game, verbose=False):
  """Function printing policy diversity within game's known policies.

  Warning : only works with deterministic policies.
  Args:
    policies: List of list of policies (One list per game player)
    game: OpenSpiel game object.
    verbose: Whether to print policy diversity information. (True : print)

  Returns:
    List of list of unique policies (One list per player)
  """
  states_dict = get_all_states.get_all_states(game, np.inf, False, False)
  unique_policies = []
  for player in range(len(policies)):
    cur_policies = policies[player]
    cur_set = set()
    for pol in cur_policies:
      cur_str = ""
      for state_str in states_dict:
        if states_dict[state_str].current_player() == player:
          pol_action_dict = pol(states_dict[state_str])
          max_prob = max(list(pol_action_dict.values()))
          max_prob_actions = [
              a for a in pol_action_dict if pol_action_dict[a] == max_prob
          ]
          cur_str += "__" + state_str
          for a in max_prob_actions:
            cur_str += "-" + str(a)
      cur_set.add(cur_str)
    unique_policies.append(cur_set)
  if verbose:
    print("\n=====================================\nPolicy Diversity :")
    for player, cur_set in enumerate(unique_policies):
      print("Player {} : {} unique policies.".format(player, len(cur_set)))
  print("")
  return unique_policies

