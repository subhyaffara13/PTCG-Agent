
def test_subsets():
    # combinations
    assert list(subsets([1, 2, 3], 0)) == [()]
    assert list(subsets([1, 2, 3], 1)) == [(1,), (2,), (3,)]
    assert list(subsets([1, 2, 3], 2)) == [(1, 2), (1, 3), (2, 3)]
    assert list(subsets([1, 2, 3], 3)) == [(1, 2, 3)]
    l = list(range(4))
    assert list(subsets(l, 0, repetition=True)) == [()]
    assert list(subsets(l, 1, repetition=True)) == [(0,), (1,), (2,), (3,)]
    assert list(subsets(l, 2, repetition=True)) == [(0, 0), (0, 1), (0, 2),
                                                    (0, 3), (1, 1), (1, 2),
                                                    (1, 3), (2, 2), (2, 3),
                                                    (3, 3)]
    assert list(subsets(l, 3, repetition=True)) == [(0, 0, 0), (0, 0, 1),
                                                    (0, 0, 2), (0, 0, 3),
                                                    (0, 1, 1), (0, 1, 2),
                                                    (0, 1, 3), (0, 2, 2),
                                                    (0, 2, 3), (0, 3, 3),
                                                    (1, 1, 1), (1, 1, 2),
                                                    (1, 1, 3), (1, 2, 2),
                                                    (1, 2, 3), (1, 3, 3),
                                                    (2, 2, 2), (2, 2, 3),
                                                    (2, 3, 3), (3, 3, 3)]
    assert len(list(subsets(l, 4, repetition=True))) == 35

    assert list(subsets(l[:2], 3, repetition=False)) == []
    assert list(subsets(l[:2], 3, repetition=True)) == [(0, 0, 0),
                                                        (0, 0, 1),
                                                        (0, 1, 1),
                                                        (1, 1, 1)]
    assert list(subsets([1, 2], repetition=True)) == \
        [(), (1,), (2,), (1, 1), (1, 2), (2, 2)]
    assert list(subsets([1, 2], repetition=False)) == \
        [(), (1,), (2,), (1, 2)]
    assert list(subsets([1, 2, 3], 2)) == \
        [(1, 2), (1, 3), (2, 3)]
    assert list(subsets([1, 2, 3], 2, repetition=True)) == \
        [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]


def test_subsets():
    assert subsets(1) == [[1]]
    assert subsets(4) == [
        [1, 0, 0, 0], [0, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 0], [1, 0, 1, 0],
        [0, 1, 1, 0], [1, 1, 1, 0], [0, 0, 0, 1], [1, 0, 0, 1], [0, 1, 0, 1],
        [1, 1, 0, 1], [0, 0, 1, 1], [1, 0, 1, 1], [0, 1, 1, 1], [1, 1, 1, 1]]


def test_subsets(n):
    elements = get_elements(n)
    dis = DisjointSet(elements)

    rng = np.random.RandomState(seed=0)
    for i, j in rng.randint(0, n, (n, 2)):
        x = elements[i]
        y = elements[j]

        expected = {element for element in dis if {dis[element]} == {dis[x]}}
        assert dis.subset_size(x) == len(dis.subset(x))
        assert expected == dis.subset(x)

        expected = {dis[element]: set() for element in dis}
        for element in dis:
            expected[dis[element]].add(element)
        expected = list(expected.values())
        assert expected == dis.subsets()

        dis.merge(x, y)
        assert dis.subset(x) == dis.subset(y)

