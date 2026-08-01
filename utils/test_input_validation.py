
def test_input_validation():
    class Test(ContinuousDistribution):
        _variable = _RealParameter('x', domain=_RealInterval())

    message = ("The `Test` distribution family does not accept parameters, "
               "but parameters `{'a'}` were provided.")
    with pytest.raises(ValueError, match=message):
        Test(a=1, )

    message = "Attribute `tol` of `Test` must be a positive float, if specified."
    with pytest.raises(ValueError, match=message):
        Test(tol=np.asarray([]))
    with pytest.raises(ValueError, match=message):
        Test(tol=[1, 2, 3])
    with pytest.raises(ValueError, match=message):
        Test(tol=np.nan)
    with pytest.raises(ValueError, match=message):
        Test(tol=-1)

    message = ("Argument `order` of `Test.moment` must be a "
               "finite integer greater than or equal to 0.")
    with pytest.raises(ValueError, match=message):
        Test().moment(-1)
    with pytest.raises(ValueError, match=message):
        Test().moment(np.inf)

    message = ("Argument `order` of `Test.lmoment` must be a "
               "finite integer greater than or equal to 1.")
    with pytest.raises(ValueError, match=message):
        Test().lmoment(0)

    message = "Argument `kind` of `Test.moment` must be one of..."
    with pytest.raises(ValueError, match=message):
        Test().moment(2, kind='coconut')

    class Test2(ContinuousDistribution):
        _p1 = _RealParameter('c', domain=_RealInterval())
        _p2 = _RealParameter('d', domain=_RealInterval())
        _parameterizations = [_Parameterization(_p1, _p2)]
        _variable = _RealParameter('x', domain=_RealInterval())

    message = ("The provided parameters `{a}` do not match a supported "
               "parameterization of the `Test2` distribution family.")
    with pytest.raises(ValueError, match=message):
        Test2(a=1)

    message = ("The `Test2` distribution family requires parameters, but none "
               "were provided.")
    with pytest.raises(ValueError, match=message):
        Test2()

    message = ("The parameters `{c, d}` provided to the `Test2` "
               "distribution family cannot be broadcast to the same shape.")
    with pytest.raises(ValueError, match=message):
        Test2(c=[1, 2], d=[1, 2, 3])

    message = ("The argument provided to `Test2.pdf` cannot be be broadcast to "
              "the same shape as the distribution parameters.")
    with pytest.raises(ValueError, match=message):
        dist = Test2(c=[1, 2, 3], d=[1, 2, 3])
        dist.pdf([1, 2])

    message = "Parameter `c` must be of real dtype."
    with pytest.raises(TypeError, match=message):
        Test2(c=[1, object()], d=[1, 2])

    message = "Parameter `convention` of `Test2.kurtosis` must be one of..."
    with pytest.raises(ValueError, match=message):
        dist = Test2(c=[1, 2, 3], d=[1, 2, 3])
        dist.kurtosis(convention='coconut')


def test_input_validation(xp):
    # Test invalid matrix shapes
    inputs = [xp.eye(3), xp.zeros((4, 3)), []]
    for input in inputs:
        with pytest.raises(ValueError, match="Expected `matrix` to have shape"):
            RigidTransform.from_matrix(input)

    # Test invalid last row
    for ndim in range(3):
        shape = (ndim,) * (ndim - 1)
        matrix = xp.zeros(shape + (4, 4))
        matrix = xpx.at(matrix)[...].set(xp.eye(4))
        matrix = xpx.at(matrix)[..., 3, :].set(xp.asarray([1.0, 0, 0, 1]))
        if is_lazy_array(matrix):
            matrix = RigidTransform.from_matrix(matrix).as_matrix()
            assert xp.all(xp.isnan(matrix[..., 3, :]))
        else:
            with pytest.raises(ValueError, match="last row of transformation matrix"):
                RigidTransform.from_matrix(matrix)

    # Test left handed rotation matrix
    matrix = xp.eye(4)
    matrix = xpx.at(matrix)[0, 0].set(-1)
    if is_lazy_array(matrix):
        matrix = RigidTransform.from_matrix(matrix).as_matrix()
        assert xp.all(xp.isnan(matrix[..., :3, :3]))
    else:
        with pytest.raises(ValueError, match="Non-positive determinant"):
            RigidTransform(matrix, normalize=True)

    # Test non-Rotation input
    with pytest.raises(TypeError,
                       match="Expected `rotation` to be a `Rotation` instance"):
        RigidTransform.from_rotation(xp.eye(3))

