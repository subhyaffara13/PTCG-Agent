
def _rollout_until_timeout(game_name,
                           time_limit,
                           give_up_after,
                           if_simultaneous_convert_to_turn_based=False):
  """Run rollouts on the specified game until the time limit.

  Args:
    game_name:      str
    time_limit:     In number of seconds
    give_up_after:  Cuts off trajectories longer than specified
    if_simultaneous_convert_to_turn_based: if the game is simultaneous and this
      boolean is true, then the game is loaded as a turn based game.

  Returns:
    A dict of collected statistics.
  """
  game = pyspiel.load_game(game_name)
  if game.get_type().dynamics == pyspiel.GameType.Dynamics.MEAN_FIELD:
    raise NotImplementedError(
        "Benchmark on mean field games is not available yet.")
  if (game.get_type().dynamics == pyspiel.GameType.Dynamics.SIMULTANEOUS and
      if_simultaneous_convert_to_turn_based):
    game = pyspiel.convert_to_turn_based(game)
  is_time_out = lambda t: time.time() - t > time_limit
  num_rollouts = 0
  num_giveups = 0
  num_moves = 0
  start = time.time()
  while not is_time_out(start):
    state = game.new_initial_state()
    while not state.is_terminal():
      if len(state.history()) > give_up_after:
        num_giveups += 1
        break
      if state.is_simultaneous_node():

        def random_choice(actions):
          if actions:
            return random.choice(actions)
          return 0

        actions = [
            random_choice(state.legal_actions(i))
            for i in range(state.num_players())
        ]
        state.apply_actions(actions)
      else:
        action = random.choice(state.legal_actions(state.current_player()))
        state.apply_action(action)
      num_moves += 1
    num_rollouts += 1
  time_elapsed = time.time() - start
  return dict(
      game_name=game_name,
      ms_per_rollouts=time_elapsed / num_rollouts * 1000,
      ms_per_moves=time_elapsed / num_moves * 1000,
      giveups_per_rollout=num_giveups / num_rollouts,
      time_elapsed=time_elapsed
  )

