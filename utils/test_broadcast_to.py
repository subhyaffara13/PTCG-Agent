
def test_broadcast_to():
    a = np.array([[1, 0, 2]])
    b = np.array([[1], [0], [2]])
    c = np.array([[1, 0, 2], [0, 3, 0]])
    d = np.array([[7]])
    e = np.array([[0]])
    f = np.array([[0,0,0,0]])
    for container in (csc_matrix, csc_array, csr_matrix, csr_array):
        res_a = container(a)._broadcast_to((2,3))
        res_b = container(b)._broadcast_to((3,4))
        res_c = container(c)._broadcast_to((2,3))
        res_d = container(d)._broadcast_to((4,4))
        res_e = container(e)._broadcast_to((5,6))
        res_f = container(f)._broadcast_to((2,4))
        assert_array_equal(res_a.toarray(), np.broadcast_to(a, (2,3)))
        assert_array_equal(res_b.toarray(), np.broadcast_to(b, (3,4)))
        assert_array_equal(res_c.toarray(), c)
        assert_array_equal(res_d.toarray(), np.broadcast_to(d, (4,4)))
        assert_array_equal(res_e.toarray(), np.broadcast_to(e, (5,6)))
        assert_array_equal(res_f.toarray(), np.broadcast_to(f, (2,4)))

        with pytest.raises(ValueError, match="cannot be broadcast"):
            container([[1, 2, 0], [3, 0, 1]])._broadcast_to(shape=(2, 1))

        with pytest.raises(ValueError, match="cannot be broadcast"):
            container([[0, 1, 2]])._broadcast_to(shape=(3, 2))


def test_broadcast_to(actual_shape, broadcast_shape):
    rng = np.random.default_rng(23409823)

    arr = random_array(actual_shape, density=0.6, random_state=rng, dtype=int)
    res = arr._broadcast_to(broadcast_shape)
    exp = np.broadcast_to(arr.toarray(), broadcast_shape)
    assert_equal(res.toarray(), exp)


def test_broadcast_to():
    a = np.array([1, 0, 2])
    b = np.array([3])
    e = np.zeros((0,))
    res_a = csr_array(a)._broadcast_to((2,3))
    res_b = csr_array(b)._broadcast_to((4,))
    res_c = csr_array(b)._broadcast_to((2,4))
    res_d = csr_array(b)._broadcast_to((1,))
    res_e = csr_array(e)._broadcast_to((4,0))
    assert_array_equal(res_a.toarray(), np.broadcast_to(a, (2,3)))
    assert_array_equal(res_b.toarray(), np.broadcast_to(b, (4,)))
    assert_array_equal(res_c.toarray(), np.broadcast_to(b, (2,4)))
    assert_array_equal(res_d.toarray(), np.broadcast_to(b, (1,)))
    assert_array_equal(res_e.toarray(), np.broadcast_to(e, (4,0)))

    with pytest.raises(ValueError, match="cannot be broadcast"):
        csr_matrix([[1, 2, 0], [3, 0, 1]])._broadcast_to(shape=(2, 1))

    with pytest.raises(ValueError, match="cannot be broadcast"):
        csr_matrix([[0, 1, 2]])._broadcast_to(shape=(3, 2))

    with pytest.raises(ValueError, match="cannot be broadcast"):
        csr_array([0, 1, 2])._broadcast_to(shape=(3, 2))

