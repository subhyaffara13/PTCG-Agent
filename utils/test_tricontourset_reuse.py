
def test_tricontourset_reuse():
    # If TriContourSet returned from one tricontour(f) call is passed as first
    # argument to another the underlying C++ contour generator will be reused.
    x = [0.0, 0.5, 1.0]
    y = [0.0, 1.0, 0.0]
    z = [1.0, 2.0, 3.0]
    fig, ax = plt.subplots()
    tcs1 = ax.tricontourf(x, y, z)
    tcs2 = ax.tricontour(x, y, z)
    assert tcs2._contour_generator != tcs1._contour_generator
    tcs3 = ax.tricontour(tcs1, z)
    assert tcs3._contour_generator == tcs1._contour_generator

