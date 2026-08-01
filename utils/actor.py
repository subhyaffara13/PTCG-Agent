
def actor(
    *,
    config: Config,
    game: pyspiel.Game,
    logger: Any,
    queue: spawn._ProcessQueue,
) -> None:
  """An actor process runner that generates games and returns trajectories."""
  logger.print("Initializing model")
  model = _init_model_from_config(config)
  logger.print("Initializing bots")
  az_evaluator = evaluator_lib.AlphaZeroEvaluator(game, model)
  bots = [
      _init_bot(config, game, az_evaluator, False),
      _init_bot(config, game, az_evaluator, False),
  ]
  for game_num in itertools.count(1):
    if not update_checkpoint(logger, queue, model, az_evaluator):
      return
    queue.put(
        _play_game(
            logger,
            game_num,
            game,
            bots,
            config.temperature,
            config.temperature_drop,
        )
    )

