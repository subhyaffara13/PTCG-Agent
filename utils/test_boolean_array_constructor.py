
def test_boolean_array_constructor():
    values = np.array([True, False, True, False], dtype="bool")
    mask = np.array([False, False, False, True], dtype="bool")

    result = BooleanArray(values, mask)
    expected = pd.array([True, False, True, None], dtype="boolean")
    tm.assert_extension_array_equal(result, expected)

    with pytest.raises(TypeError, match="values should be boolean numpy array"):
        BooleanArray(values.tolist(), mask)

    with pytest.raises(TypeError, match="mask should be boolean numpy array"):
        BooleanArray(values, mask.tolist())

    with pytest.raises(TypeError, match="values should be boolean numpy array"):
        BooleanArray(values.astype(int), mask)

    with pytest.raises(TypeError, match="mask should be boolean numpy array"):
        BooleanArray(values, None)

    with pytest.raises(ValueError, match="values.shape must match mask.shape"):
        BooleanArray(values.reshape(1, -1), mask)

    with pytest.raises(ValueError, match="values.shape must match mask.shape"):
        BooleanArray(values, mask.reshape(1, -1))

