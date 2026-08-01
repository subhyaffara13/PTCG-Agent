
def test_generic_data_series(adaptive):
    # verify that no errors are raised when generic data series are used
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x = Symbol("x")
    p = plot(x,
        markers=[{"args":[[0, 1], [0, 1]], "marker": "*", "linestyle": "none"}],
        annotations=[{"text": "test", "xy": (0, 0)}],
        fill={"x": [0, 1, 2, 3], "y1": [0, 1, 2, 3]},
        rectangles=[{"xy": (0, 0), "width": 5, "height": 1}],
        adaptive=adaptive, n=10)
    assert len(p._backend.ax.collections) == 1
    assert len(p._backend.ax.patches) == 1
    assert len(p._backend.ax.lines) == 2
    assert len(p._backend.ax.texts) == 1

