import copy

def test_round_trip(m):
    assert_equal_tensor_ref(m.round_trip_tensor(tensor_ref))

    with pytest.raises(TypeError, match="^Cannot cast array data from"):
        assert_equal_tensor_ref(m.round_trip_tensor2(tensor_ref))

    assert_equal_tensor_ref(m.round_trip_tensor2(np.array(tensor_ref, dtype=np.int32)))
    assert_equal_tensor_ref(m.round_trip_fixed_tensor(tensor_ref))
    assert_equal_tensor_ref(m.round_trip_aligned_view_tensor(m.reference_tensor()))

    copy = np.array(tensor_ref, dtype=np.float64, order=m.needed_options)
    assert_equal_tensor_ref(m.round_trip_view_tensor(copy))
    assert_equal_tensor_ref(m.round_trip_view_tensor_ref(copy))
    assert_equal_tensor_ref(m.round_trip_view_tensor_ptr(copy))
    copy.setflags(write=False)
    assert_equal_tensor_ref(m.round_trip_const_view_tensor(copy))

    np.testing.assert_array_equal(
        tensor_ref[:, ::-1, :], m.round_trip_tensor(tensor_ref[:, ::-1, :])
    )

    assert m.round_trip_rank_0(np.float64(3.5)) == 3.5
    assert m.round_trip_rank_0(3.5) == 3.5

    with pytest.raises(
        TypeError,
        match=r"^round_trip_rank_0_noconvert\(\): incompatible function arguments",
    ):
        m.round_trip_rank_0_noconvert(np.float64(3.5))

    with pytest.raises(
        TypeError,
        match=r"^round_trip_rank_0_noconvert\(\): incompatible function arguments",
    ):
        m.round_trip_rank_0_noconvert(3.5)

    with pytest.raises(
        TypeError, match=r"^round_trip_rank_0_view\(\): incompatible function arguments"
    ):
        m.round_trip_rank_0_view(np.float64(3.5))

    with pytest.raises(
        TypeError, match=r"^round_trip_rank_0_view\(\): incompatible function arguments"
    ):
        m.round_trip_rank_0_view(3.5)


def test_round_trip():
    def doit(t, b):
        e, n = Prufer.edges(*t)
        t = Prufer(e, n)
        a = sorted(t.tree_repr)
        b = [i - 1 for i in b]
        assert t.prufer_repr == b
        assert sorted(Prufer(b).tree_repr) == a
        assert Prufer.unrank(t.rank, n).prufer_repr == b

    doit([[1, 2]], [])
    doit([[2, 1, 3]], [1])
    doit([[1, 3, 2]], [3])
    doit([[1, 2, 3]], [2])
    doit([[2, 1, 4], [1, 3]], [1, 1])
    doit([[3, 2, 1, 4]], [2, 1])
    doit([[3, 2, 1], [2, 4]], [2, 2])
    doit([[1, 3, 2, 4]], [3, 2])
    doit([[1, 4, 2, 3]], [4, 2])
    doit([[3, 1, 4, 2]], [4, 1])
    doit([[4, 2, 1, 3]], [1, 2])
    doit([[1, 2, 4, 3]], [2, 4])
    doit([[1, 3, 4, 2]], [3, 4])
    doit([[2, 4, 1], [4, 3]], [4, 4])
    doit([[1, 2, 3, 4]], [2, 3])
    doit([[2, 3, 1], [3, 4]], [3, 3])
    doit([[1, 4, 3, 2]], [4, 3])
    doit([[2, 1, 4, 3]], [1, 4])
    doit([[2, 1, 3, 4]], [1, 3])
    doit([[6, 2, 1, 4], [1, 3, 5, 8], [3, 7]], [1, 2, 1, 3, 3, 5])


def test_round_trip(version, fmts):
    for case in _cases(version, filt=None):
        for fmt in fmts:
            _rt_check_case(case[0], case[2], fmt)

