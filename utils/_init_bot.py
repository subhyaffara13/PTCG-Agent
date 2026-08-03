from typing import Any

def _init_bot(bot_type, game, player_id):
  """Initializes a bot by type.

  Args:
    bot_type: The string type of the bot (e.g. "mcts", "random").
    game: The pyspiel game object.
    player_id: The integer id of the player.

  Returns:
    A bot object (e.g. mcts.MCTSBot).
  """
  rng = np.random.RandomState(FLAGS.seed)
  if bot_type == "mcts":
    evaluator = mcts.RandomRolloutEvaluator(FLAGS.rollout_count, rng)
    return mcts.MCTSBot(
        game,
        FLAGS.uct_c,
        FLAGS.max_simulations,
        evaluator,
        random_state=rng,
        solve=FLAGS.solve,
        verbose=FLAGS.verbose)
  if bot_type == "random":
    return uniform_random.UniformRandomBot(player_id, rng)
  if bot_type == "human":
    return human.HumanBot()
  if bot_type == "gtp":
    bot = gtp.GTPBot(game, FLAGS.gtp_path)
    for cmd in FLAGS.gtp_cmd:
      bot.gtp_cmd(cmd)
    return bot
  raise ValueError("Invalid bot type: %s" % bot_type)


def _init_bot(
    config: Config, game: Any, evaluator_: mcts.Evaluator, evaluation: bool
) -> mcts.MCTSBot:
  """Initialises a MCTS bot."""
  noise = None if evaluation else (config.policy_epsilon, config.policy_alpha)
  return mcts.MCTSBot(
      game,
      config.uct_c,
      config.max_simulations,
      evaluator_,
      solve=False,
      dirichlet_noise=noise,
      child_selection_fn=mcts.SearchNode.puct_value,
      verbose=config.verbose,
      dont_return_chance_node=True,
  )

