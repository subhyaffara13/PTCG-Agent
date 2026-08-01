
def test_patch_bounds():  # PR 19078
    fig, ax = plt.subplots()
    ax.add_patch(mpatches.Wedge((0, -1), 1.05, 60, 120, width=0.1))
    bot = 1.9*np.sin(15*np.pi/180)**2
    np.testing.assert_array_almost_equal_nulp(
        np.array((-0.525, -(bot+0.05), 1.05, bot+0.1)), ax.dataLim.bounds, 16)

