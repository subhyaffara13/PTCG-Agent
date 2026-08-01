
def test_shapes_solve_like(func, core_shape):
    # test shapes for solve-like functions, where the 2nd argument may have trailing
    # dimensions
    m, n = core_shape

    # ### 1. a.ndim == 2 ###

    # 1.1 : b.ndim == 1, the "scalar" case
    a = np.eye(m, n)
    b = np.ones(m)

    x = func(a, b)
    assert x.shape == (n,)

    # 1.2 : b.ndim == 2 : b has trailing dims
    b = np.ones((m, 8))
    x = func(a, b)
    assert x.shape == (n, 8)

    # 1.3 : b.ndim == 3 : b has trailing dims *and* batch dims
    b = np.ones((4, m, 8))
    x = func(a, b)
    assert x.shape == (4, n, 8)

    # 1.4 : b.ndim == 2 : b has batch dims *but* no trailing dims
    b = np.ones((4, m))
    pattern = "Shape mismatch|incompatible shapes|shapes of a|shape mismatch"
    with pytest.raises(ValueError, match=pattern):
        # fails to broadcast `b` vs `a` (to fix: append a length-1 trailing dim)
        func(a, b)

    # ### 2. a.ndim > 2 ###
    a = np.broadcast_to(a, (5, 4, *a.shape))  # batch_shape = (5, 4)

    # 2.1 : b is 1D
    b = np.ones(m)
    x = func(a, b)
    assert x.shape == (5, 4, n)

    # 2.2 : b.ndim == 2, has trailing dims
    b = np.ones((m, 8))
    x = func(a, b)
    assert x.shape == (5, 4, n, 8)

    # 2.3 : b has both trailing and batch dims
    b = np.ones((5, 4, m, 8))
    x = func(a, b)
    assert x.shape == (5, 4, n, 8)

    # 2.3.1 : b has trailing dims and (broadcastable) batch dims
    b = np.ones((4, m, 8))
    x = func(a, b)
    assert x.shape == (5, 4, n, 8)

    # 2.4 : b has batch dims but no trailing dims
    b = np.ones((5, 4, m))
    pattern = "Shape mismatch|incompatible shapes|shapes of a|shape mismatch"
    with pytest.raises(ValueError, match=pattern):
        # fails to broadcast `b` vs `a` (to fix: append a length-1 trailing dim)
        func(a, b)

