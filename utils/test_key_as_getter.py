
def test_key_as_getter():
    squares = [(i, i**2) for i in range(5)]
    pows = [(i, i**2, i**3) for i in range(5)]

    assert set(join(0, squares, 0, pows)) == set(join(lambda x: x[0], squares,
                                                      lambda x: x[0], pows))

    get = lambda x: (x[0], x[1])
    assert set(join([0, 1], squares, [0, 1], pows)) == set(join(get, squares,
                                                                get, pows))

    get = lambda x: (x[0],)
    assert set(join([0], squares, [0], pows)) == set(join(get, squares,
                                                          get, pows))

