
def test_mult_norm_call_types():
    mn = mpl.colors.MultiNorm(['linear', 'linear'])
    mn.vmin = (-2, -2)
    mn.vmax = (2, 2)

    vals = np.arange(6).reshape((3,2))
    target = np.ma.array([(0.5, 0.75),
                          (1., 1.25),
                          (1.5, 1.75)])

    # test structured array as input
    from_mn = mn(rfn.unstructured_to_structured(vals))
    assert_array_almost_equal(from_mn,
                              target.T)

    # test list of arrays as input
    assert_array_almost_equal(mn(list(vals.T)),
                              list(target.T))
    # test list of floats as input
    assert_array_almost_equal(mn(list(vals[0])),
                              list(target[0]))
    # test tuple of arrays as input
    assert_array_almost_equal(mn(tuple(vals.T)),
                              list(target.T))

    # np.arrays of shapes that are compatible
    assert_array_almost_equal(mn(np.zeros(2)),
                              0.5*np.ones(2))
    assert_array_almost_equal(mn(np.zeros((2, 3))),
                              0.5*np.ones((2, 3)))
    assert_array_almost_equal(mn(np.zeros((2, 3, 4))),
                              0.5*np.ones((2, 3, 4)))

    # test with NoNorm, list as input
    mn_no_norm = mpl.colors.MultiNorm(['linear', mcolors.NoNorm()])
    no_norm_out = mn_no_norm(list(vals.T))
    assert_array_almost_equal(no_norm_out,
                              [[0., 0.5, 1.],
                               [1, 3, 5]])
    assert no_norm_out[0].dtype == np.dtype('float64')
    assert no_norm_out[1].dtype == vals.dtype

    # test with NoNorm, structured array as input
    mn_no_norm = mpl.colors.MultiNorm(['linear', mcolors.NoNorm()])
    no_norm_out = mn_no_norm(rfn.unstructured_to_structured(vals))
    assert_array_almost_equal(no_norm_out,
                              [[0., 0.5, 1.],
                               [1, 3, 5]])

    # test single int as input
    with pytest.raises(ValueError,
                       match="component as input, but got 1 instead"):
        mn(1)

    # test list of incompatible size
    with pytest.raises(ValueError,
                       match="but got a sequence with 3 elements"):
        mn([3, 2, 1])

    # last axis matches, len(data.shape) > 2
    with pytest.raises(ValueError,
                       match=(r"`data_as_list = \[data\[..., i\] for i in "
                              r"range\(data.shape\[-1\]\)\]`")):
        mn(np.zeros((3, 3, 2)))

    # last axis matches, len(data.shape) == 2
    with pytest.raises(ValueError,
                       match=r"You can use `data_transposed = data.T` to convert"):
        mn(np.zeros((3, 2)))

    # incompatible arrays where no relevant axis matches
    for data in [np.zeros(3), np.zeros((3, 2, 3))]:
        with pytest.raises(ValueError,
                           match=r"but got a sequence with 3 elements"):
            mn(data)

    # test incompatible class
    with pytest.raises(ValueError,
                       match="but got <object object"):
        mn(object())

