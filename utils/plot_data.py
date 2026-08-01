
def plot_data(config, data):
  """Plot a bunch of graphs from an alphazero experiment."""
  num_rows, num_cols = 3, 4
  x = X_AXIS[FLAGS.x_axis]

  fig = plt.figure(figsize=(num_cols * 7, num_rows * 6))
  fig.suptitle(
      (
          "Game: {}, Model: {}({}, {}), training time: {}, training steps: {}, "
          "states: {}, games: {}"
      ).format(
          config["game"],
          config["nn_model"],
          config["nn_width"],
          config["nn_depth"],
          datetime.timedelta(seconds=int(data[-1]["time_rel"])),
          int(data[-1]["step"]),
          int(data[-1]["total_states"]),
          int(data[-1]["total_trajectories"]),
      )
  )

  cols = ["value", "policy", "l2reg", "sum"]
  df = prepare(data, {v: ["loss", v] for v in cols})
  ax = subplot(num_rows, num_cols, 1, title="Training loss")
  for y in cols:
    df.plot(ax=ax, x=x, y=y)

  cols = list(range(len(data[0]["value_accuracy"])))
  df = prepare(data, {i: ["value_accuracy", i, "avg"] for i in cols})
  ax = subplot(
      num_rows,
      num_cols,
      2,  # ylim=(0, 1.05),
      title="MCTS value prediction accuracy",
  )
  for y in cols:
    df.plot(ax=ax, x=x, y=y)

  cols = list(range(len(data[0]["value_prediction"])))
  df = prepare(data, {i: ["value_prediction", i, "avg"] for i in cols})
  ax = subplot(
      num_rows,
      num_cols,
      3,  # ylim=(0, 1.05),
      title="MCTS absolute value prediction",
  )
  for y in cols:
    df.plot(ax=ax, x=x, y=y)

  cols = list(range(len(data[0]["eval"]["results"])))
  df = prepare(data, {i: ["eval", "results", i] for i in cols})
  ax = subplot(
      num_rows,
      num_cols,
      4,
      ylim=(-1, 1),
      title="Evaluation returns vs MCTS+Solver with x10^(n/2) sims",
  )
  ax.axhline(y=0, color="black")
  for y in cols:
    df.plot(ax=ax, x=x, y=y)

  df = prepare(data, {"states_per_s_actor": ["states_per_s_actor"]})
  ax = subplot(num_rows, num_cols, 5, title="Speed of actor state/s")
  df.plot(ax=ax, x=x, y="states_per_s_actor")
  plot_zero(df, ax, x)

  cols = ["requests_per_s", "misses_per_s"]
  df = prepare(data, {v: ["cache", v] for v in cols})
  ax = subplot(num_rows, num_cols, 6, title="Cache requests/s")
  for y in cols:
    df.plot(ax=ax, x=x, y=y)
  plot_zero(df, ax, x)

  cols = ["hit_rate", "usage"]
  df = prepare(data, {v: ["cache", v] for v in cols})
  ax = subplot(
      num_rows, num_cols, 7, title="Cache usage and hit rate.", ylim=(0, 1.05)
  )
  for y in cols:
    df.plot(ax=ax, x=x, y=y)

  ax = subplot(num_rows, num_cols, 8, title="Outcomes", ylim=(0, 1))
  plot_histogram_named(ax, x, data, ["outcomes"])

  ax = subplot(
      num_rows, num_cols, 9, title="Inference batch size + stddev + min/max"
  )
  plot_avg_stddev(ax, x, data, ["batch_size"])

  ax = subplot(num_rows, num_cols, 10, title="Inference batch size")
  plot_histogram_numbered(ax, x, data, ["batch_size_hist"])

  ax = subplot(num_rows, num_cols, 11, title="Game length + stddev + min/max")
  plot_avg_stddev(ax, x, data, ["game_length"])

  ax = subplot(num_rows, num_cols, 12, title="Game length histogram")
  plot_histogram_numbered(ax, x, data, ["game_length_hist"])

  plt.show()

