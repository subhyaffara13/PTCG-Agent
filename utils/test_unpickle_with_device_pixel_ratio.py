
def test_unpickle_with_device_pixel_ratio():
    fig = Figure(dpi=42)
    fig.canvas._set_device_pixel_ratio(7)
    assert fig.dpi == 42*7
    fig2 = pickle.loads(pickle.dumps(fig))
    assert fig2.dpi == 42
    assert all(
        [orig / 7 == restore for orig, restore in zip(fig.bbox.max, fig2.bbox.max)]
    )

