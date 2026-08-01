
def test_bounds_with_list():
    # gh13501. Bounds created with lists weren't working for Powell.
    bounds = optimize.Bounds(lb=[5., 5.], ub=[10., 10.])
    optimize.minimize(
        optimize.rosen, x0=np.array([9, 9]), method='Powell', bounds=bounds
    )

