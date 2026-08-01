
def turn_based_example(unused_arg):
  """Example usage of the RL environment for turn-based games."""
  # `rl_main_loop.py` contains more details and simultaneous move examples.
  logging.info("Registered games: %s", rl_environment.registered_games())
  logging.info("Creating game %s", FLAGS.game)

  env_configs = {"players": FLAGS.num_players} if FLAGS.num_players else {}
  env = rl_environment.Environment(FLAGS.game, **env_configs)

  logging.info("Env specs: %s", env.observation_spec())
  logging.info("Action specs: %s", env.action_spec())

  time_step = env.reset()

  while not time_step.step_type.last():
    pid = time_step.observations["current_player"]
    actions = select_actions(time_step.observations, pid)
    print_iteration(time_step, actions, pid)
    time_step = env.step(actions)

  # Print final state of end game.
  for pid in range(env.num_players):
    print_iteration(time_step, actions, pid)

