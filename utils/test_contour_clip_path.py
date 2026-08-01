
def test_contour_clip_path():
    fig, ax = plt.subplots()
    data = [[0, 1], [1, 0]]
    circle = mpatches.Circle([0.5, 0.5], 0.5, transform=ax.transAxes)
    cs = ax.contour(data, clip_path=circle)
    assert cs.get_clip_path() is not None

