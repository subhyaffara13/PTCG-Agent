
def test_numpy_view(capture):
    with capture:
        ac = m.ArrayClass()
        ac_view_1 = ac.numpy_view()
        ac_view_2 = ac.numpy_view()
        assert np.all(ac_view_1 == np.array([1, 2], dtype=np.int32))
        del ac
        pytest.gc_collect()
    assert (
        capture
        == """
        ArrayClass()
        ArrayClass::numpy_view()
        ArrayClass::numpy_view()
    """
    )
    ac_view_1[0] = 4
    ac_view_1[1] = 3
    assert ac_view_2[0] == 4
    assert ac_view_2[1] == 3
    with capture:
        del ac_view_1
        del ac_view_2
        pytest.gc_collect()
        pytest.gc_collect()
    assert (
        capture
        == """
        ~ArrayClass()
    """
    )

