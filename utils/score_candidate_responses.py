
def score_candidate_responses(game_str, config, load_dict, rnd,
                              background_policies, candidates,
                              player_ids=(0,), num_trials=5):
  """Simulate a batch of dialogues and returns payoffs for each player."""

  num_players = config.params["num_players"]

  num_candidates = len(candidates)

  config.game.given_prompt_actions["tone"] += candidates
  num_actions = len(config.game.given_prompt_actions["tone"])
  config.params["num_distinct_actions"] = num_players * num_actions

  game = pyspiel.load_game(game_str, config.params.to_dict())

  game.load_chat_game(**load_dict, **config.game)

  payoffs = np.zeros((num_trials, len(player_ids), num_candidates))

  for player_id in player_ids:
    for trial in range(num_trials):
      for candidate_idx in range(num_candidates):
        policies = []
        for i in range(num_players):
          if player_id == i:
            fixed_tone = {"tone": candidates[candidate_idx]}
            policy = lambda state: fixed_prompt_policy(rnd, state, fixed_tone)  # pylint:disable=cell-var-from-loop
            policies.append(policy)
          else:
            policies.append(background_policies[i])
        player_policy = build_player_policy(policies)

        returns = simulate_dialogue(game, player_policy)

        payoffs[trial, player_id, candidate_idx] = returns[player_id]

  # undo changes to config (is this inplace?)
  config.game.given_prompt_actions["tone"] = config.game.given_prompt_actions[
      "tone"
  ][:-num_candidates]
  num_tones = len(config.game.given_prompt_actions["tone"])
  config.params["num_distinct_actions"] = num_players * num_tones

  return payoffs, candidates

