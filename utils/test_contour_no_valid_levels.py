
def test_contour_no_valid_levels():
    fig, ax = plt.subplots()
    # no warning for empty levels.
    ax.contour(np.random.rand(9, 9), levels=[])
    # no warning if levels is given and is not within the range of z.
    cs = ax.contour(np.arange(81).reshape((9, 9)), levels=[100])
    # ... and if fmt is given.
    ax.clabel(cs, fmt={100: '%1.2f'})
    # no warning if z is uniform.
    ax.contour(np.ones((9, 9)))

