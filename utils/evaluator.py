
def evaluator(
    *, game: pyspiel.Game, config: Config, logger: Any, queue
) -> None:
  """A process that plays the latest checkpoint vs standard MCTS."""
  results = buffer_lib.Buffer(config.evaluation_window, force_cpu=True)

  logger.print("Initializing model")
  model = _init_model_from_config(config)
  logger.print("Initializing bots")
  az_evaluator = evaluator_lib.AlphaZeroEvaluator(game, model)
  random_evaluator = mcts.RandomRolloutEvaluator()

  for game_num in itertools.count():
    if not update_checkpoint(logger, queue, model, az_evaluator):
      return

    az_player = game_num % 2
    difficulty = (game_num // 2) % config.eval_levels
    max_simulations = int(config.max_simulations * (10 ** (difficulty / 2)))
    bots = [
        _init_bot(config, game, az_evaluator, True),
        mcts.MCTSBot(
            game,
            config.uct_c,
            max_simulations,
            random_evaluator,
            solve=True,
            verbose=config.verbose,
            dont_return_chance_node=True,
        ),
    ]
    if az_player == 1:
      bots = list(reversed(bots))

    trajectory = _play_game(
        logger, game_num, game, bots, temperature=1, temperature_drop=0
    )
    results.append(jnp.asarray(trajectory.returns[az_player]))
    queue.put((difficulty, jnp.asarray(trajectory.returns[az_player])))

    logger.print(
        f"AZ: {trajectory.returns[az_player]},      MCTS:"
        f" {trajectory.returns[1 - az_player]},      AZ avg/{len(results)}:"
        f" {jnp.mean(results.data):.3f}"
    )

