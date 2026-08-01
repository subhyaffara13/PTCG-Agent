
def plot_histogram_numbered(ax, x, data, data_col):
  """Plot stats produced by open_spiel::HistogramNumbered::ToJson."""
  x_min, x_max = 0, data[-1][x]
  y_min, y_max = 0, len(subselect(data, [0] + data_col))
  z_min, z_max = 0, 1
  z = np.array([subselect(row, data_col) for row in data], dtype=float)
  z = np.concatenate((z, np.zeros((x_max, 1))), axis=1)  # Don't cut off the top
  # TODO(author7): smoothing
  z = sub_sample(z, SUBSAMPLING_MAX).transpose()
  p = np.percentile(z, 99)
  if p > 0:
    z /= p
    z[z > 1] = 1
  ax.grid(False)
  ax.imshow(
      z,
      cmap="Reds",
      vmin=z_min,
      vmax=z_max,
      extent=[x_min, x_max, y_min, y_max + 1],
      interpolation="nearest",
      origin="lower",
      aspect="auto",
  )

