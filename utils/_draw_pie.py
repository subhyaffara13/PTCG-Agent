
def _draw_pie(ax,
              ratios,
              colors,
              x_center=0,
              y_center=0,
              size=100,
              clip_on=True,
              zorder=0):
  """Plots a pie chart.

  Args:
    ax: plot axis.
    ratios: list indicating size of each pie slice, with elements summing to 1.
    colors: list indicating color of each pie slice.
    x_center: x coordinate of pie center.
    y_center: y coordinate of pie center.
    size: pie size.
    clip_on: control clipping of pie (e.g., to show it when it's out of axis).
    zorder: plot z order (e.g., to show pie on top of other plot elements).
  """
  xy = []
  start = 0.
  for ratio in ratios:
    x = [0] + np.cos(
        np.linspace(2 * np.pi * start, 2 * np.pi *
                    (start + ratio), 30)).tolist()
    y = [0] + np.sin(
        np.linspace(2 * np.pi * start, 2 * np.pi *
                    (start + ratio), 30)).tolist()
    xy.append(list(zip(x, y)))
    start += ratio

  for i, xyi in enumerate(xy):
    ax.scatter([x_center], [y_center],
               marker=xyi,
               s=size,
               facecolor=colors[i],
               edgecolors="none",
               clip_on=clip_on,
               zorder=zorder)

