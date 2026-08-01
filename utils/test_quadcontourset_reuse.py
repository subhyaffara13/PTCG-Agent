
def test_quadcontourset_reuse():
    # If QuadContourSet returned from one contour(f) call is passed as first
    # argument to another the underlying C++ contour generator will be reused.
    x, y = np.meshgrid([0.0, 1.0], [0.0, 1.0])
    z = x + y
    fig, ax = plt.subplots()
    qcs1 = ax.contourf(x, y, z)
    qcs2 = ax.contour(x, y, z)
    assert qcs2._contour_generator != qcs1._contour_generator
    qcs3 = ax.contour(qcs1, z)
    assert qcs3._contour_generator == qcs1._contour_generator

