
def test_init():
    n = 10
    elements = get_elements(n)
    dis = DisjointSet(elements)
    assert dis.n_subsets == n
    assert list(dis) == elements

