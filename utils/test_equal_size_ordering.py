
def test_equal_size_ordering(n, order):
    elements = get_elements(n)
    dis = DisjointSet(elements)

    rng = np.random.RandomState(seed=0)
    indices = np.arange(n)
    rng.shuffle(indices)

    for i in range(0, len(indices), 2):
        a, b = elements[indices[i]], elements[indices[i + 1]]
        if order == "ab":
            assert dis.merge(a, b)
        else:
            assert dis.merge(b, a)

        expected = elements[min(indices[i], indices[i + 1])]
        assert dis[a] == expected
        assert dis[b] == expected

