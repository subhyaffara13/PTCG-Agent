
def learner(
    *,
    game: pyspiel.Game,
    config: Config,
    actors: list[spawn.Process],
    evaluators: list[spawn.Process],
    broadcast_fn: Callable,
    logger: Any,
) -> None:
  """A learner that consumes the replay buffer and trains the network."""
  logger.also_to_stdout = True

  replay_buffer = buffer_lib.Buffer(config.replay_buffer_size)
  learn_rate = config.replay_buffer_size // config.replay_buffer_reuse
  logger.print("Initializing model")
  model = _init_model_from_config(config)
  logger.print(
      f"Model type: {config.nn_model}({config.nn_width}, {config.nn_depth})"
  )
  logger.print("Model size:", model.num_trainable_variables, "variables")

  save_path = model.save_checkpoint(0)
  logger.print("Initial checkpoint:", save_path)
  broadcast_fn(str(save_path))

  data_log = data_logger.DataLoggerJsonLines(config.path, "learner", True)

  stage_count = config.eval_levels
  value_accuracies = [stats.BasicStats() for _ in range(stage_count)]
  value_predictions = [stats.BasicStats() for _ in range(stage_count)]
  game_lengths = stats.BasicStats()
  game_lengths_hist = stats.HistogramNumbered(game.max_game_length() + 1)
  outcomes = stats.HistogramNamed(["Player1", "Player2", "Draw"])
  # evaluation is yet on cpu
  evals = [
      buffer_lib.Buffer(config.evaluation_window, force_cpu=True)
      for _ in range(config.eval_levels)
  ]
  total_trajectories = 0

  def trajectory_generator():
    """Merge all the actor queues into a single generator."""
    while True:
      found = 0
      for actor_process in actors:
        try:
          yield actor_process.queue.get_nowait()
        except spawn.Empty:
          pass
        else:
          found += 1
      if found == 0:
        time.sleep(0.01)  # 10ms

  def collect_trajectories() -> tuple[int, int]:
    """Collects the trajectories from actors into the replay buffer."""

    logger.print("Collecting trajectories")
    num_trajectories = 0
    num_states = 0
    for trajectory in trajectory_generator():
      num_trajectories += 1
      num_states += len(trajectory.states)
      game_lengths.add(len(trajectory.states))
      game_lengths_hist.add(len(trajectory.states))

      # we learn from perspective of only the first player,
      # rather than rotating
      game_outcome = trajectory.returns[0]
      if game_outcome > 0:
        outcomes.add(0)
      elif game_outcome < 0:
        outcomes.add(1)
      else:
        outcomes.add(2)

      for s in trajectory.states:
        replay_buffer.append(
            utils.TrainInput(
                observation=jnp.asarray(s.observation, dtype=jnp.float32),
                legals_mask=jnp.asarray(s.legals_mask, dtype=jnp.bool),
                policy=jnp.asarray(s.policy, dtype=jnp.float32),
                value=jnp.asarray(game_outcome, dtype=jnp.float32),
            )
        )

      for stage in range(stage_count):
        # Scale for the length of the game
        index = (len(trajectory.states) - 1) * stage // (stage_count - 1)
        n = trajectory.states[index]
        # Replaced by the MSE to get a smoother estimate of the value learning
        value_accuracies[stage].add(
            (n.value - trajectory.returns[n.current_player]) ** 2
        )
        value_predictions[stage].add(abs(n.value))

      if num_states >= learn_rate:
        break
    return num_trajectories, num_states

  def learn(step: int | str) -> tuple[str, utils.Losses]:
    """Sample from the replay buffer, update weights and save a checkpoint."""
    losses = []
    for _ in range(len(replay_buffer) // config.train_batch_size):
      data = replay_buffer.sample(config.train_batch_size)
      losses.append(model.update(data))

    # Always save a checkpoint, either for keeping or for loading the weights to
    # the actors. We only allow numbers, so use -1 as the "latest".
    save_path = model.save_checkpoint(
        step if step % config.checkpoint_freq == 0 else -1
    )

    # for an unlucky case when the agent hasn't collected enough transitions
    if losses:
      losses = sum(losses, utils.Losses(policy=0, value=0, l2=0)) / len(losses)
    else:
      losses = utils.Losses(policy=0, value=0, l2=0)

    logger.print(losses)
    logger.print("Checkpoint saved:", save_path)
    return save_path, losses

  last_time = time.time() - 60
  for step in itertools.count(1):
    for value_accuracy in value_accuracies:
      value_accuracy.reset()
    for value_prediction in value_predictions:
      value_prediction.reset()
    game_lengths.reset()
    game_lengths_hist.reset()
    outcomes.reset()

    num_trajectories, num_states = collect_trajectories()
    total_trajectories += num_trajectories
    now = time.time()
    seconds = now - last_time
    last_time = now

    logger.print("Step:", step)
    logger.print((
        f"Collected {num_states:5} states from {num_trajectories:3} games, "
        f"{(num_states / seconds):.1f} states/s. "
        f"{(num_states / (config.actors * seconds)):.1f} states/(s*actor), "
        f"game length: {(num_states / num_trajectories):.1f}"
    ))
    logger.print(
        f"Buffer size: {len(replay_buffer)}. States seen:"
        f" {replay_buffer.total_seen}"
    )

    save_path, losses = learn(step)

    for eval_process in evaluators:
      while True:
        try:
          difficulty, outcome = eval_process.queue.get_nowait()
          evals[difficulty].append(outcome)
        except spawn.Empty:
          break

    batch_size_stats = stats.BasicStats()  # Only makes sense in C++.
    batch_size_stats.add(1)
    data_log.write({
        "step": step,
        "total_states": replay_buffer.total_seen,
        "states_per_s_actor": num_states / (config.actors * seconds),
        "total_trajectories": total_trajectories,
        "trajectories_per_s": num_trajectories / seconds,
        "queue_size": 0,  # Only available in C++.
        "game_length": game_lengths.as_dict,
        "game_length_hist": game_lengths_hist.data,
        "outcomes": outcomes.data,
        "value_accuracy": [v.as_dict for v in value_accuracies],
        "value_prediction": [v.as_dict for v in value_predictions],
        "eval": {
            "count": evals[0].total_seen,
            "results": [np.mean(e.data).item() if e else 0 for e in evals],
        },
        "batch_size": batch_size_stats.as_dict,
        "batch_size_hist": [0, 1],
        "loss": {
            "policy": float(losses.policy),
            "value": float(losses.value),
            "l2reg": float(losses.l2),
            "sum": float(losses.total),
        },
        "cache": {  # Null stats because it's hard to report between processes.
            "size": 0,
            "max_size": 0,
            "usage": 0,
            "requests": 0,
            "requests_per_s": 0,
            "hits": 0,
            "misses": 0,
            "misses_per_s": 0,
            "hit_rate": 0,
        },
    })
    logger.print()

    if config.max_steps > 0 and step >= config.max_steps:
      break

    broadcast_fn(str(save_path))

