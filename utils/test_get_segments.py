
def test_get_segments():
    segments = np.tile(np.linspace(0, 1, 256), (2, 1)).T
    lc = LineCollection([segments])

    readback, = lc.get_segments()
    # these should comeback un-changed!
    assert np.all(segments == readback)

