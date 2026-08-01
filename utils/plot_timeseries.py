
def plot_timeseries(ax, id_ax, data, xticks, xlabel='', ylabel='',
                    label='', logx=False, logy=False, zorder=10,
                    linespecs=None):
  """Plots timeseries data with error bars."""
  if logx:
    ax[id_ax].set_xscale('log')
  if logy:
    ax[id_ax].set_yscale('log')
  if linespecs:
    kwargs = {'color': linespecs['color']}
  else:
    kwargs = {}

  # Seaborn's bootstrapped confidence intervals were used in the original paper
  se = scipy.stats.sem(data, axis=0)
  ax[id_ax].fill_between(xticks, data.mean(0)-se, data.mean(0)+se,
                         zorder=zorder, alpha=0.2, **kwargs)
  ax[id_ax].plot(xticks, data.mean(0), label=label, zorder=zorder, **kwargs)

  # There may be multiple lines on the current axis, some from previous calls to
  # plot_timeseries, so reference just the latest
  if linespecs:
    ax[id_ax].get_lines()[-1].set_dashes([5, 5])
    ax[id_ax].get_lines()[-1].set_linestyle(linespecs['linestyle'])

  ax[id_ax].set(xlabel=xlabel, ylabel=ylabel)
  ax[id_ax].set_axisbelow(True)
  ax[id_ax].grid(True)
  for _, spine in ax[id_ax].spines.items():
    spine.set_zorder(-1)

