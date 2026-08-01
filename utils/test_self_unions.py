
def test_self_unions(n):
    elements = get_elements(n)
    dis = DisjointSet(elements)

    for x in elements:
        assert dis.connected(x, x)
        assert not dis.merge(x, x)
        assert dis.connected(x, x)
    assert dis.n_subsets == len(elements)

    assert elements == list(dis)
    roots = [dis[x] for x in elements]
    assert elements == roots

