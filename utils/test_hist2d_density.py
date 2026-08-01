
def test_hist2d_density():
    x, y = np.random.random((2, 100))
    ax = plt.figure().subplots()
    for obj in [ax, plt]:
        obj.hist2d(x, y, density=True)

