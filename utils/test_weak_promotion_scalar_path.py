
def test_weak_promotion_scalar_path(op):
    # Some additional paths exercising the weak scalars.

    # Integer path:
    res = op(np.uint8(3), 5)
    assert res == op(3, 5)
    assert res.dtype == np.uint8 or res.dtype == bool

    with pytest.raises(OverflowError):
        op(np.uint8(3), 1000)

    # Float path:
    res = op(np.float32(3), 5.)
    assert res == op(3., 5.)
    assert res.dtype == np.float32 or res.dtype == bool

