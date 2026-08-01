
def plot_network_mean_field_game(g: dynamic_routing_utils.Network,
                                 distribution=None,
                                 scaling=1):
  """Plot the network.

  Args:
    g: network to plot
    distribution: the distribution.
    scaling: scaling factor. for plot rendering.
  """
  _, ax = plt.subplots()
  o_xs, o_ys, d_xs, d_ys = g.return_list_for_matplotlib_quiver()
  ax.quiver(
      o_xs,
      o_ys,
      np.subtract(d_xs, o_xs),
      np.subtract(d_ys, o_ys),
      color="b",
      angles="xy",
      scale_units="xy",
      scale=1)
  ax.set_xlim([
      np.min(np.concatenate((o_xs, d_xs))) - 0.5,
      np.max(np.concatenate((o_xs, d_xs))) + 0.5
  ])
  ax.set_ylim([
      np.min(np.concatenate((o_ys, d_ys))) - 0.5,
      np.max(np.concatenate((o_ys, d_ys))) + 0.5
  ])

  if distribution is not None:
    for x, prob_of_position in distribution.items():
      point = g.return_position_of_road_section(x)
      width = 0.3 * scaling * prob_of_position
      circle = plt.Circle(point, width, color="r")
      ax.add_patch(circle)

