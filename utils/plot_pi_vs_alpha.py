
def plot_pi_vs_alpha(pi_list,
                     alpha_list,
                     num_populations,
                     num_strats_per_population,
                     strat_labels,
                     num_strats_to_label,
                     plot_semilogx=True,
                     xlabel=r"Ranking-intensity $\alpha$",
                     ylabel=r"Strategy mass in stationary distribution $\pi$",
                     legend_sort_clusters=False):
  """Plots stationary distributions, pi, against selection intensities, alpha.

  Args:
    pi_list: List of stationary distributions, pi.
    alpha_list: List of selection intensities, alpha.
    num_populations: The number of populations.
    num_strats_per_population: List of the number of strategies per population.
    strat_labels: Human-readable strategy labels.
    num_strats_to_label: The number of top strategies to label in the legend.
    plot_semilogx: Boolean set to enable/disable semilogx plot.
    xlabel: Plot xlabel.
    ylabel: Plot ylabel.
    legend_sort_clusters: If true, strategies in the same cluster are sorted in
      the legend according to orderings for earlier alpha values. Primarily for
      visualization purposes! Rankings for lower alpha values should be
      interpreted carefully.
  """

  # Cluster strategies for which the stationary distribution has similar masses
  masses_to_strats = utils.cluster_strats(pi_list[-1, :])

  # Set colors
  num_strat_profiles = np.shape(pi_list)[1]
  num_strats_to_label = min(num_strats_to_label, num_strat_profiles)
  cmap = plt.get_cmap("Paired")
  colors = [cmap(i) for i in np.linspace(0, 1, num_strat_profiles)]

  # Plots stationary distribution vs. alpha series
  plt.figure(facecolor="w")
  axes = plt.gca()

  legend_line_objects = []
  legend_labels = []

  rank = 1
  num_strats_printed = 0
  add_legend_entries = True

  if legend_sort_clusters:
    sorted_masses_strats = generate_sorted_masses_strats(
        pi_list, pi_list.shape[0] - 1, range(pi_list.shape[1]))
  else:
    sorted_masses_strats = sorted(masses_to_strats.items(), reverse=True)

  for mass, strats in sorted_masses_strats:
    for profile_id in strats:
      if num_populations == 1:
        strat_profile = profile_id
      else:
        strat_profile = utils.get_strat_profile_from_id(
            num_strats_per_population, profile_id)

      if plot_semilogx:
        series = plt.semilogx(
            alpha_list,
            pi_list[:, profile_id],
            color=colors[profile_id],
            linewidth=2)
      else:
        series = plt.plot(
            alpha_list,
            pi_list[:, profile_id],
            color=colors[profile_id],
            linewidth=2)

      if add_legend_entries:
        if num_strats_printed >= num_strats_to_label:
          # Placeholder blank series for remaining entries
          series = plt.semilogx(np.nan, np.nan, "-", color="none")
          label = "..."
          add_legend_entries = False
        else:
          label = utils.get_label_from_strat_profile(num_populations,
                                                     strat_profile,
                                                     strat_labels)
        legend_labels.append(label)
        legend_line_objects.append(series[0])
      num_strats_printed += 1
    rank += 1

  # Plots pie charts on far right of figure to indicate clusters of strategies
  # with identical rank
  for mass, strats in iter(masses_to_strats.items()):
    _draw_pie(
        axes,
        ratios=[1 / len(strats)] * len(strats),
        colors=[colors[i] for i in strats],
        x_center=alpha_list[-1],
        y_center=mass,
        size=200,
        clip_on=False,
        zorder=10)

  # Axes ymax set slightly above highest stationary distribution mass
  max_mass = np.amax(pi_list)
  axes_y_max = np.ceil(
      10. * max_mass) / 10  # Round upward to nearest first decimal
  axes_y_max = np.clip(axes_y_max, 0., 1.)

  # Plots a rectangle highlighting the rankings on the far right of the figure
  box_x_min = alpha_list[-1] * 0.7
  box_y_min = np.min(pi_list[-1, :]) - 0.05 * axes_y_max
  width = 0.7 * alpha_list[-1]
  height = np.max(pi_list[-1, :]) - np.min(
      pi_list[-1, :]) + 0.05 * axes_y_max * 2
  axes.add_patch(
      patches.Rectangle((box_x_min, box_y_min),
                        width,
                        height,
                        edgecolor="b",
                        facecolor=(1, 0, 0, 0),
                        clip_on=False,
                        linewidth=5,
                        zorder=20))

  # Plot formatting
  axes.set_xlim(np.min(alpha_list), np.max(alpha_list))
  axes.set_ylim([0.0, axes_y_max])
  axes.set_xlabel(xlabel)
  axes.set_ylabel(ylabel)
  axes.set_axisbelow(True)  # Axes appear below data series in terms of zorder

  # Legend on the right side of the current axis
  box = axes.get_position()
  axes.set_position([box.x0, box.y0, box.width * 0.8, box.height])
  axes.legend(
      legend_line_objects,
      legend_labels,
      loc="center left",
      bbox_to_anchor=(1.05, 0.5))
  plt.grid()
  plt.show()

