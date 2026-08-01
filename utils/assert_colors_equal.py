
def assert_colors_equal(a, b, check_alpha=True):

    def handle_array(x):

        if isinstance(x, np.ndarray):
            if x.ndim > 1:
                x = np.unique(x, axis=0).squeeze()
            if x.ndim > 1:
                raise ValueError("Color arrays must be 1 dimensional")
        return x

    a = handle_array(a)
    b = handle_array(b)

    f = to_rgba if check_alpha else to_rgb
    assert f(a) == f(b)

