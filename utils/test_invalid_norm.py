
def test_invalid_norm(func):
    x = np.arange(10, dtype=float)
    with assert_raises(ValueError,
                       match='Invalid norm value \'o\', should be'
                             ' "backward", "ortho" or "forward"'):
        func(x, norm='o')

