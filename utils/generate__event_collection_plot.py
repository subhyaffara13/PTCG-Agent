
def generate_EventCollection_plot():
    """Generate the initial collection and plot it."""
    positions = np.array([0., 1., 2., 3., 5., 8., 13., 21.])
    extra_positions = np.array([34., 55., 89.])
    orientation = 'horizontal'
    lineoffset = 1
    linelength = .5
    linewidth = 2
    color = [1, 0, 0, 1]
    linestyle = 'solid'
    antialiased = True

    coll = EventCollection(positions,
                           orientation=orientation,
                           lineoffset=lineoffset,
                           linelength=linelength,
                           linewidth=linewidth,
                           color=color,
                           linestyle=linestyle,
                           antialiased=antialiased
                           )

    fig, ax = plt.subplots()
    ax.add_collection(coll)
    ax.set_title('EventCollection: default')
    props = {'positions': positions,
             'extra_positions': extra_positions,
             'orientation': orientation,
             'lineoffset': lineoffset,
             'linelength': linelength,
             'linewidth': linewidth,
             'color': color,
             'linestyle': linestyle,
             'antialiased': antialiased
             }
    ax.set_xlim(-1, 22)
    ax.set_ylim(0, 2)
    return ax, coll, props

