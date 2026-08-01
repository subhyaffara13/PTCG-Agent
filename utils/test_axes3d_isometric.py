
def test_axes3d_isometric():
    from itertools import combinations, product
    fig, ax = plt.subplots(subplot_kw=dict(
        projection='3d',
        proj_type='ortho',
        box_aspect=(4, 4, 4)
    ))
    r = (-1, 1)  # stackoverflow.com/a/11156353
    for s, e in combinations(np.array(list(product(r, r, r))), 2):
        if abs(s - e).sum() == r[1] - r[0]:
            ax.plot3D(*zip(s, e), c='k')
    ax.view_init(elev=np.degrees(np.arctan(1. / np.sqrt(2))), azim=-45, roll=0)
    ax.grid(True)

