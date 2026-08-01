
def test_fancyarrow_dash():
    fig, ax = plt.subplots()
    e = mpatches.FancyArrowPatch((0, 0), (0.5, 0.5),
                                 arrowstyle='-|>',
                                 connectionstyle='angle3,angleA=0,angleB=90',
                                 mutation_scale=10.0,
                                 linewidth=2,
                                 linestyle='dashed',
                                 color='k')
    e2 = mpatches.FancyArrowPatch((0, 0), (0.5, 0.5),
                                  arrowstyle='-|>',
                                  connectionstyle='angle3',
                                  mutation_scale=10.0,
                                  linewidth=2,
                                  linestyle='dotted',
                                  color='k')
    ax.add_patch(e)
    ax.add_patch(e2)

