
def test_dense_constructor_with_inconsistent_shape():
    with pytest.raises(ValueError, match='inconsistent shapes'):
        coo_array([1, 2, 3], shape=(4,))

    with pytest.raises(ValueError, match='inconsistent shapes'):
        coo_array([1, 2, 3], shape=(3, 1))

    with pytest.raises(ValueError, match='inconsistent shapes'):
        coo_array([[1, 2, 3]], shape=(3,))

    with pytest.raises(ValueError, match='inconsistent shapes'):
        coo_array([[[3]], [[4]]], shape=(1, 1, 1))

    with pytest.raises(ValueError,
                       match='axis 0 index 2 exceeds matrix dimension 2'):
        coo_array(([1], ([2],)), shape=(2,))

    with pytest.raises(ValueError,
                       match='axis 1 index 3 exceeds matrix dimension 3'):
        coo_array(([1,3], ([0, 1], [0, 3], [1, 1])), shape=(2, 3, 2))

    with pytest.raises(ValueError, match='negative axis 0 index: -1'):
        coo_array(([1], ([-1],)))

    with pytest.raises(ValueError, match='negative axis 2 index: -1'):
        coo_array(([1], ([0], [2], [-1])))

