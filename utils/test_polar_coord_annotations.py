
def test_polar_coord_annotations():
    # You can also use polar notation on a cartesian axes.  Here the native
    # coordinate system ('data') is cartesian, so you need to specify the
    # xycoords and textcoords as 'polar' if you want to use (theta, radius).
    el = mpl.patches.Ellipse((0, 0), 10, 20, facecolor='r', alpha=0.5)

    fig = plt.figure()
    ax = fig.add_subplot(aspect='equal')

    ax.add_artist(el)
    el.set_clip_box(ax.bbox)

    ax.annotate('the top',
                xy=(np.pi/2., 10.),      # theta, radius
                xytext=(np.pi/3, 20.),   # theta, radius
                xycoords='polar',
                textcoords='polar',
                arrowprops=dict(facecolor='black', shrink=0.05),
                horizontalalignment='left',
                verticalalignment='baseline',
                clip_on=True,  # clip to the axes bounding box
                )

    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)

