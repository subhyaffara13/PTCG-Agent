
def test_ensure_multivariate_data():

    # text complex input
    for dtype, target in zip(["complex64", "complex128"], [np.float32, np.float64]):
        data = np.arange(12).reshape((4, 3)).astype(dtype)
        mdata = mcolorizer._ensure_multivariate_data(data, 2)
        assert mdata.shape == (4, 3)
        assert mdata.dtype.fields['f0'][0] == target
        assert mdata.dtype.fields['f1'][0] == target
        assert_array_almost_equal(mdata["f0"], np.arange(12).reshape((4, 3)))
        assert_array_almost_equal(mdata["f1"], np.zeros(12).reshape((4, 3)))

    # test complex masked
    data = np.arange(12).reshape((4, 3)).astype('complex128')
    data = np.ma.masked_where(data > 5, data)
    mdata = mcolorizer._ensure_multivariate_data(data, 2)
    assert np.all(mdata["f0"].mask[:2] == 0)
    assert np.all(mdata["f0"].mask[2:] == 1)
    assert np.all(mdata["f1"].mask[:2] == 0)
    assert np.all(mdata["f1"].mask[2:] == 1)

    # test tuple of data
    data = [0, 1]
    mdata = mcolorizer._ensure_multivariate_data(data, 2)
    assert mdata.shape == ()

    # test wrong input size
    data = [[0, 1]]
    with pytest.raises(ValueError, match="must contain complex numbers"):
        mcolorizer._ensure_multivariate_data(data, 2)
    data = [[0, 1]]
    with pytest.raises(ValueError, match="have a first dimension 3"):
        mcolorizer._ensure_multivariate_data(data, 3)

    # test input of ints as list of lists
    data = [[0, 0, 0], [1, 1, 1]]
    mdata = mcolorizer._ensure_multivariate_data(data, 2)
    assert mdata.shape == (3,)
    assert mdata.dtype.fields['f0'][0] == np.int_
    assert mdata.dtype.fields['f1'][0] == np.int_

    # test input of floats, ints as tuple of lists
    data = ([0.0, 0.0], [1, 1])
    mdata = mcolorizer._ensure_multivariate_data(data, 2)
    assert mdata.shape == (2,)
    assert mdata.dtype.fields['f0'][0] == np.float64
    assert mdata.dtype.fields['f1'][0] == np.int_

    # test input of array of floats
    data = np.array([[0.0, 0, 0], [1, 1, 1]])
    mdata = mcolorizer._ensure_multivariate_data(data, 2)
    assert mdata.shape == (3,)
    assert mdata.dtype.fields['f0'][0] == np.float64
    assert mdata.dtype.fields['f1'][0] == np.float64

    # test more input dims
    data = np.zeros((3, 4, 5, 6))
    mdata = mcolorizer._ensure_multivariate_data(data, 3)
    assert mdata.shape == (4, 5, 6)

