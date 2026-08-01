
def eval_checkpoint(roshambo_bot_names, prediction_logger):
  """Evaluate a checkpoint."""

  print("Starting eval checkpoint")
  print("Loading checkpoint")
  checkpoint = Checkpoint(FLAGS.eval_checkpoint)
  checkpoint.restore_or_save()
  assert checkpoint.state.learning_agents is not None
  print("Checkpoint loaded")
  greenberg_bot = pyspiel.make_roshambo_bot(1, "greenberg")
  greenberg_agent = BotAgent(3, greenberg_bot, name="greenberg_agent")
  print("Starting eval for agent...")
  env = rl_environment.Environment(
      "repeated_game(stage_game=matrix_rps(),num_repetitions="
      + f"{pyspiel.ROSHAMBO_NUM_THROWS},"
      + f"recall={FLAGS.env_recall})",
      include_full_state=True,
  )
  sum_eval_returns = np.zeros(pyspiel.ROSHAMBO_NUM_BOTS)
  for j in range(50):
    print(f"Eval checkpoint, j={j}")
    _, pop_expl = eval_agent(
        env,
        2,
        3,
        roshambo_bot_names,
        # checkpoint.state.learning_agents[1],
        greenberg_agent,
        prediction_logger,
        0,
    )
    eval_returns = (-1) * pop_expl
    sum_eval_returns += eval_returns
    avg_eval_returns = sum_eval_returns / (j + 1)
    pop_return = avg_eval_returns.sum() / pyspiel.ROSHAMBO_NUM_BOTS
    wp_expl = avg_eval_returns.min() * (-1)
    print(f"Pop return: {pop_return}, WP expl: {wp_expl}")
    print(avg_eval_returns)

