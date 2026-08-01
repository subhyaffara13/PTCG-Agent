
def test_splprep_segfault():
    # regression test for gh-3847: splprep segfaults if knots are specified
    # for task=-1
    t = np.arange(0, 1.1, 0.1)
    x = np.sin(2*np.pi*t)
    y = np.cos(2*np.pi*t)
    tck, u = splprep([x, y], s=0)
    np.arange(0, 1.01, 0.01)

    uknots = tck[0]  # using the knots from the previous fitting
    tck, u = splprep([x, y], task=-1, t=uknots)  # here is the crash

