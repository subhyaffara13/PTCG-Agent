
def test_pinv_rtol_arg():
    a = np.array([[1, 2, 3], [4, 1, 1], [2, 3, 1]])

    assert_almost_equal(
        np.linalg.pinv(a, rcond=0.5),
        np.linalg.pinv(a, rtol=0.5),
    )

    with pytest.raises(
        ValueError, match=r"`rtol` and `rcond` can't be both set."
    ):
        np.linalg.pinv(a, rcond=0.5, rtol=0.5)

