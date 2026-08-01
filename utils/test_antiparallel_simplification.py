
def test_antiparallel_simplification():
    def _get_simplified(x, y):
        fig, ax = plt.subplots()
        p1 = ax.plot(x, y)

        path = p1[0].get_path()
        transform = p1[0].get_transform()
        path = transform.transform_path(path)
        simplified = path.cleaned(simplify=True)
        simplified = transform.inverted().transform_path(simplified)

        return simplified

    # test ending on a maximum
    x = [0, 0, 0, 0, 0, 1]
    y = [.5, 1, -1, 1, 2, .5]

    simplified = _get_simplified(x, y)

    assert_array_almost_equal([[0., 0.5],
                               [0., -1.],
                               [0., 2.],
                               [1., 0.5]],
                              simplified.vertices[:-2, :])

    # test ending on a minimum
    x = [0, 0,  0, 0, 0, 1]
    y = [.5, 1, -1, 1, -2, .5]

    simplified = _get_simplified(x, y)

    assert_array_almost_equal([[0., 0.5],
                               [0., 1.],
                               [0., -2.],
                               [1., 0.5]],
                              simplified.vertices[:-2, :])

    # test ending in between
    x = [0, 0, 0, 0, 0, 1]
    y = [.5, 1, -1, 1, 0, .5]

    simplified = _get_simplified(x, y)

    assert_array_almost_equal([[0., 0.5],
                               [0., 1.],
                               [0., -1.],
                               [0., 0.],
                               [1., 0.5]],
                              simplified.vertices[:-2, :])

    # test no anti-parallel ending at max
    x = [0, 0, 0, 0, 0, 1]
    y = [.5, 1, 2, 1, 3, .5]

    simplified = _get_simplified(x, y)

    assert_array_almost_equal([[0., 0.5],
                               [0., 3.],
                               [1., 0.5]],
                              simplified.vertices[:-2, :])

    # test no anti-parallel ending in middle
    x = [0, 0, 0, 0, 0, 1]
    y = [.5, 1, 2, 1, 1, .5]

    simplified = _get_simplified(x, y)

    assert_array_almost_equal([[0., 0.5],
                               [0., 2.],
                               [0., 1.],
                               [1., 0.5]],
                              simplified.vertices[:-2, :])

