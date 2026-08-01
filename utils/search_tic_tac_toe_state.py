
def search_tic_tac_toe_state(initial_actions):
  game = pyspiel.load_game("tic_tac_toe")
  state = game.new_initial_state()
  for action_str in initial_actions.split(" "):
    state.apply_action(_get_action(state, action_str))
  rng = np.random.RandomState(42)
  bot = async_mcts.MCTSBot(
      game,
      UCT_C,
      max_simulations=10000,
      solve=True,
      random_state=rng,
      evaluator=async_mcts.RandomRolloutEvaluator(random_state=rng),
  )
  return bot.mcts_search(state), state


def search_tic_tac_toe_state(initial_actions):
  game = pyspiel.load_game("tic_tac_toe")
  state = game.new_initial_state()
  for action_str in initial_actions.split(" "):
    state.apply_action(_get_action(state, action_str))
  rng = np.random.RandomState(42)
  bot = mcts.MCTSBot(
      game,
      UCT_C,
      max_simulations=10000,
      solve=True,
      random_state=rng,
      evaluator=mcts.RandomRolloutEvaluator(n_rollouts=20, random_state=rng))
  return bot.mcts_search(state), state

