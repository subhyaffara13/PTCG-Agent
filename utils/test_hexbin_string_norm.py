
def test_hexbin_string_norm():
    fig, ax = plt.subplots()
    hex = ax.hexbin(np.random.rand(10), np.random.rand(10), norm="log", vmin=2, vmax=5)
    assert isinstance(hex, matplotlib.collections.PolyCollection)
    assert isinstance(hex.norm, matplotlib.colors.LogNorm)
    assert hex.norm.vmin == 2
    assert hex.norm.vmax == 5

