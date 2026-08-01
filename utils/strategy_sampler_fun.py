
def strategy_sampler_fun(total_policies, probabilities_of_playing_policies):
  """Samples strategies according to distribution over them.

  Args:
    total_policies: List of lists of policies for each player.
    probabilities_of_playing_policies: List of numpy arrays representing the
      probability of playing a strategy.

  Returns:
    One sampled joint strategy.
  """
  policies_selected = []
  for k in range(len(total_policies)):
    selected_opponent = np.random.choice(
        total_policies[k],
        1,
        p=probabilities_of_playing_policies[k]).reshape(-1)[0]
    policies_selected.append(selected_opponent)
  return policies_selected

