
def test_power_operator(A):
    assert isinstance((A**2), scipy.sparse.sparray), "Expected array, got matrix"

    # https://github.com/scipy/scipy/issues/15948
    npt.assert_equal((A**2).todense(), (A.todense())**2)

    # power of zero is all ones (dense) so helpful msg exception
    with pytest.raises(NotImplementedError, match="zero power"):
        A**0

