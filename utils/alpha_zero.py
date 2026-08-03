import json
import os
import sys

def alpha_zero(config: Config) -> None:
  # NOTE: a single device accelearation is currently supported

  """Start all the worker processes for a full alphazero setup."""
  game = pyspiel.load_game(config.game)
  config = config.replace(
      observation_shape=game.observation_tensor_shape(),
      output_size=game.num_distinct_actions(),
  )

  print("Starting game", config.game)
  if game.num_players() != 2:
    sys.exit("AlphaZero can only handle 2-player games.")
  game_type = game.get_type()
  if game_type.reward_model != pyspiel.GameType.RewardModel.TERMINAL:
    raise ValueError("Game must have terminal rewards.")
  if game_type.dynamics != pyspiel.GameType.Dynamics.SEQUENTIAL:
    raise ValueError("Game must have sequential turns.")

  path = config.path
  if not path:
    path = tempfile.mkdtemp(
        prefix="az-{}-{}-".format(
            datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"), config.game
        )
    )
    config = config.replace(path=path)

  if not os.path.exists(path):
    os.makedirs(path)
  if not os.path.isdir(path):
    sys.exit(f"{path} isn't a directory")
  print(f"Writing logs and checkpoints to: {path}")
  print(
      f"Model type: {config.nn_model}(width={config.nn_width},"
      f" depth={config.nn_depth})"
  )

  with open(os.path.join(config.path, "config.json"), "w") as fp:
    fp.write(json.dumps(config.__dict__, indent=2, sort_keys=True) + "\n")

  actors = [
      spawn.Process(actor, kwargs={"game": game, "config": config, "num": i})
      for i in range(config.actors)
  ]

  evaluators = [
      spawn.Process(
          evaluator, kwargs={"game": game, "config": config, "num": i}
      )
      for i in range(config.evaluators)
  ]

  def broadcast(msg):
    for proc in actors + evaluators:
      proc.queue.put(msg)

  try:
    learner(
        game=game,
        config=config,
        actors=actors,  # pylint: disable=missing-kwoa
        evaluators=evaluators,
        broadcast_fn=broadcast,
    )
  except (KeyboardInterrupt, EOFError):
    print("Caught a KeyboardInterrupt, stopping early.")
  finally:
    broadcast("")
    # for actor processes to join we have to make sure that their q_in is empty,
    # including backed up items
    for proc in actors:
      while proc.exitcode is None:
        while not proc.queue.empty():
          proc.queue.get_nowait()
        proc.join(JOIN_WAIT_DELAY)
    for proc in evaluators:
      proc.join()

