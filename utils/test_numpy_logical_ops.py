
def test_numpy_logical_ops():
    if not numpy:
        skip("numpy not installed.")
    and_func = lambdify((x, y), And(x, y), modules="numpy")
    and_func_3 = lambdify((x, y, z), And(x, y, z), modules="numpy")
    or_func = lambdify((x, y), Or(x, y), modules="numpy")
    or_func_3 = lambdify((x, y, z), Or(x, y, z), modules="numpy")
    not_func = lambdify((x), Not(x), modules="numpy")
    arr1 = numpy.array([True, True])
    arr2 = numpy.array([False, True])
    arr3 = numpy.array([True, False])
    numpy.testing.assert_array_equal(and_func(arr1, arr2), numpy.array([False, True]))
    numpy.testing.assert_array_equal(and_func_3(arr1, arr2, arr3), numpy.array([False, False]))
    numpy.testing.assert_array_equal(or_func(arr1, arr2), numpy.array([True, True]))
    numpy.testing.assert_array_equal(or_func_3(arr1, arr2, arr3), numpy.array([True, True]))
    numpy.testing.assert_array_equal(not_func(arr2), numpy.array([True, False]))

