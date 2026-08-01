
def plot_avg_stddev(ax, x, data, data_col):
  """Plot stats produced by open_spiel::BasicStats::ToJson."""
  cols = ["avg", "std_dev", "min", "max"]
  df = prepare(data, {v: data_col + [v] for v in cols})
  df.plot(ax=ax, x=x, y="avg", color="b")
  plt.fill_between(
      x=df[x],
      color="b",
      alpha=0.2,
      label="std dev",
      y1=np.nanmax([df["min"], df["avg"] - df["std_dev"]], 0),
      y2=np.nanmin([df["max"], df["avg"] + df["std_dev"]], 0),
  )
  plt.fill_between(
      x=df[x], color="b", alpha=0.2, label="min/max", y1=df["min"], y2=df["max"]
  )
  plot_zero(df, ax, x)

