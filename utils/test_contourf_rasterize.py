
def test_contourf_rasterize():
    fig, ax = plt.subplots()
    data = [[0, 1], [1, 0]]
    circle = mpatches.Circle([0.5, 0.5], 0.5, transform=ax.transAxes)
    cs = ax.contourf(data, clip_path=circle, rasterized=True)
    assert cs._rasterized

