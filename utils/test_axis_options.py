
def test_axis_options():
    fig, axes = plt.subplots(2, 3)
    for i, option in enumerate(('scaled', 'tight', 'image')):
        # Draw a line and a circle fitting within the boundaries of the line
        # The circle should look like a circle for 'scaled' and 'image'
        # High/narrow aspect ratio
        axes[0, i].plot((1, 2), (1, 3.2))
        axes[0, i].axis(option)
        axes[0, i].add_artist(mpatches.Circle((1.5, 1.5), radius=0.5,
                                              facecolor='none', edgecolor='k'))
        # Low/wide aspect ratio
        axes[1, i].plot((1, 2.25), (1, 1.75))
        axes[1, i].axis(option)
        axes[1, i].add_artist(mpatches.Circle((1.5, 1.25), radius=0.25,
                                              facecolor='none', edgecolor='k'))

