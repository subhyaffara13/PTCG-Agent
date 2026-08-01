
def plot_histogram_named(ax, x, data, data_col, normalized=True):
  """Plot stats produced by open_spiel::HistogramNamed::ToJson."""
  names = subselect(data, [0] + data_col + ["names"])
  df = prepare(
      data, {name: data_col + ["counts", i] for i, name in enumerate(names)}
  )
  if normalized:
    total = sum(df[n] for n in names)
    for n in names:
      df[n] /= total
  df.plot.area(ax=ax, x=x, y=names)

