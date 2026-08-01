
def test_clipping():
    exterior = mpath.Path.unit_rectangle().deepcopy()
    exterior.vertices *= 4
    exterior.vertices -= 2
    interior = mpath.Path.unit_circle().deepcopy()
    interior.vertices = interior.vertices[::-1]
    clip_path = mpath.Path.make_compound_path(exterior, interior)

    star = mpath.Path.unit_regular_star(6).deepcopy()
    star.vertices *= 2.6

    fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True, sharey=True)

    col = mcollections.PathCollection([star], lw=5, edgecolor='blue',
                                      facecolor='red', alpha=0.7, hatch='*')
    col.set_clip_path(clip_path, ax1.transData)
    ax1.add_collection(col)

    patch = mpatches.PathPatch(star, lw=5, edgecolor='blue', facecolor='red',
                               alpha=0.7, hatch='*')
    patch.set_clip_path(clip_path, ax2.transData)
    ax2.add_patch(patch)

    ax1.set_xlim(-3, 3)
    ax1.set_ylim(-3, 3)


def test_clipping():
    t = np.arange(0.0, 2.0, 0.01)
    s = np.sin(2*np.pi*t)

    fig, ax = plt.subplots()
    ax.plot(t, s, linewidth=1.0)
    ax.set_ylim(-0.20, -0.28)

