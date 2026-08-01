
def plot_network_n_player_game(g: dynamic_routing_utils.Network,
                               vehicle_locations=None):
  """Plot the network.

  Args:
    g: network to plot
    vehicle_locations: vehicle location
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

  if vehicle_locations is not None:
    num_vehicle = len(vehicle_locations)
    dict_location = {}
    for vehicle_location in vehicle_locations:
      if vehicle_location not in dict_location:
        dict_location[vehicle_location] = 0.0
      dict_location[vehicle_location] += 0.3 / num_vehicle
    for point, width in dict_location.items():
      circle = plt.Circle(point, width, color="r")
      ax.add_patch(circle)

