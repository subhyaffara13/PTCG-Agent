
def plot_cuboid(ax, scale):
    # plot a rectangular cuboid with side lengths given by scale (x, y, z)
    r = [0, 1]
    pts = itertools.combinations(np.array(list(itertools.product(r, r, r))), 2)
    for start, end in pts:
        if np.sum(np.abs(start - end)) == r[1] - r[0]:
            ax.plot3D(*zip(start*np.array(scale), end*np.array(scale)))

