
def test_hexbin_log_clim():
    x, y = np.arange(200).reshape((2, 100))
    fig, ax = plt.subplots()
    h = ax.hexbin(x, y, bins='log', vmin=2, vmax=100)
    assert h.get_clim() == (2, 100)

