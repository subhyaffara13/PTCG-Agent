
def test_tuple_constructor_for_dim_size_zero():
    # arrays with a dimension of size 0
    with pytest.raises(ValueError, match='exceeds matrix dimension'):
        coo_array(([9, 8], ([1, 2], [1, 0], [2, 1])), shape=(3,4,0))

    empty_arr = coo_array(([], ([], [], [], [])), shape=(4,0,2,3))
    assert_equal(empty_arr.toarray(), np.empty((4,0,2,3)))

