
def test_amin_amax_minimum_maximum():
    if not numpy:
        skip("numpy not installed")

    a234 = numpy.array([2, 3, 4])
    a152 = numpy.array([1, 5, 2])

    a254 = numpy.array([2, 5, 4])
    a132 = numpy.array([1, 3, 2])
    # 2 args
    assert numpy.all(lambdify((x, y), maximum(x, y))(a234, a152) == a254)
    assert numpy.all(lambdify((x, y), minimum(x, y))(a234, a152) == a132)

    # 3 args
    assert numpy.all(lambdify((x, y, z), maximum(x, y, z))(a234, a152, a234) == a254)
    assert numpy.all(lambdify((x, y, z), minimum(x, y, z))(a234, a152, a234) == a132)

    # 1 arg
    assert numpy.all(lambdify((x,), maximum(x))(a234) == a234)
    assert numpy.all(lambdify((x,), minimum(x))(a234) == a234)

    # 4 args, mixed length
    assert numpy.all(lambdify((x, y, z, w), maximum(x, y, z, w))(a234, a152, a234, 3) == [3, 5, 4])
    assert numpy.all(lambdify((x, y, z, w), minimum(x, y, z, w))(a234, a152, a234, 2) == [1, 2, 2])

    # amin & amax
    assert lambdify((x, y), [amin(x), amax(y)])(a234, a152) == [2, 5]
    A = numpy.array([
        [0, 4, 8],
        [1, 5, 9],
        [2, 6, 10],
    ])
    min_, max_ = lambdify((x,), [amin(x, axis=0), amax(x, axis=1)])(A)
    assert numpy.all(min_ == numpy.amin(A, axis=0))
    assert numpy.all(max_ == numpy.amax(A, axis=1))

    # see gh-25659
    assert numpy.all(lambdify((x, y), Max(x, y))([1, 2, 3], [3, 2, 1]) == [3, 2, 3])
    assert numpy.all(lambdify((x), Min(2, x))([1, 2, 3]) == [1, 2, 2])

