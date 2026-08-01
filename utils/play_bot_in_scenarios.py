
def play_bot_in_scenarios(game, bots, scenarios=None):
  """Plays a bot against a number of scenarios.

  Args:
    game: The game the bot is playing.
    bots: A list of length game.num_players() of pyspiel.Bots (or equivalent).
      Must implement the apply_action and step methods.
    scenarios: The scenarios we evaluate the bot in. A List[Scenario].

  Returns:
    A dict mapping scenarios to their scores (with an additional "mean_score"
    field containing the mean score across all scenarios).
    The average score across all scenarios.
  """
  if scenarios is None:
    scenarios = get_default_scenarios(game.get_type().short_name)

  results = []
  total_score = 0
  for scenario in scenarios:
    state = game.new_initial_state()
    bot = bots[scenario.player_id]
    bot.restart()
    for action_str in scenario.init_actions:
      action = state.string_to_action(action_str)
      if state.current_player() == scenario.player_id:
        bot.force_action(state, action)
      state.apply_action(action)
    actions_and_probs, _ = bot.step(state)
    expected_action = state.string_to_action(scenario.expected_action_str)
    for action, prob in actions_and_probs:
      if action == expected_action:
        actual_prob = prob
        break
    score = 1 - abs(actual_prob - scenario.expected_prob)
    results.append((scenario.name, score, scenario.expected_action_str,
                    scenario.expected_prob, actual_prob))
    total_score += score

  if scenarios:
    total_score /= len(scenarios)
  logging.info("Average score across all scenarios: %.4f.", total_score)
  results_dict = {}
  for name, score, expected_action, expected_prob, actual_prob in results:
    logging.info("************************************************************")
    logging.info("Scenario: '%s'. Score: %.4f.", name, score)
    logging.info("Expected action %s with probability %.4f but assigned %.4f.",
                 expected_action, expected_prob, actual_prob)
    logging.info("***************************")
    results_dict["scenario_score: " + name] = score
  results_dict["mean_score"] = total_score
  return results_dict

