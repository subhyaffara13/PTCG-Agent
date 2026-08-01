
def add_offsetboxes(ax, size=10, margin=.1, color='black'):
    """
    Surround ax with OffsetBoxes
    """
    m, mp = margin, 1+margin
    anchor_points = [(-m, -m), (-m, .5), (-m, mp),
                     (.5, mp), (mp, mp), (mp, .5),
                     (mp, -m), (.5, -m)]
    for point in anchor_points:
        da = DrawingArea(size, size)
        background = Rectangle((0, 0), width=size,
                               height=size,
                               facecolor=color,
                               edgecolor='None',
                               linewidth=0,
                               antialiased=False)
        da.add_artist(background)

        anchored_box = AnchoredOffsetbox(
            loc='center',
            child=da,
            pad=0.,
            frameon=False,
            bbox_to_anchor=point,
            bbox_transform=ax.transAxes,
            borderpad=0.)
        ax.add_artist(anchored_box)

