
def test_path_collection():
    rng = np.random.default_rng(19680801)
    xvals = rng.uniform(0, 1, 10)
    yvals = rng.uniform(0, 1, 10)
    sizes = rng.uniform(30, 100, 10)
    fig, ax = plt.subplots()
    ax.scatter(xvals, yvals, sizes, edgecolor=[0.9, 0.2, 0.1], marker='<')
    ax.set_axis_off()
    paths = [path.Path.unit_regular_polygon(i) for i in range(3, 7)]
    offsets = rng.uniform(0, 200, 20).reshape(10, 2)
    sizes = [0.02, 0.04]
    pc = mcollections.PathCollection(paths, sizes, zorder=-1,
                                     facecolors='yellow', offsets=offsets)
    # Note: autolim=False is used to keep the view limits as is for now,
    # given the updated behavior of autolim=True to also update the view
    # limits. It may be reasonable to test the limits handling in the future
    # as well. This will require regenerating the reference image.
    ax.add_collection(pc, autolim=False)
    ax.set_xlim(0, 1)

