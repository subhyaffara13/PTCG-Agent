
def estimate_payoff_tensor(game, rnd, num_trials=5):
  """Simulate a batch of dialogues and returns payoffs for each player."""

  num_players = game.num_players()
  num_actions = len(game.given_prompt_actions["tone"])
  payoff_tensor = np.zeros(
      (num_trials, num_players) + (num_actions,) * num_players
  )

  joint_actions = list(itertools.product(range(num_actions),
                                         repeat=num_players))

  for trial in range(num_trials):
    for joint_action_idx in joint_actions:
      policies = []
      for _, tone_idx in zip(range(num_players), joint_action_idx):
        fixed_tone = {"tone": game.given_prompt_actions["tone"][tone_idx]}
        policy = lambda state: fixed_prompt_policy(rnd, state, fixed_tone)  # pylint:disable=cell-var-from-loop
        policies.append(policy)
      player_policy = build_player_policy(policies)

      returns = simulate_dialogue(game, player_policy)

      pt_index = (trial, slice(None)) + joint_action_idx

      payoff_tensor[pt_index] = returns

  return payoff_tensor

