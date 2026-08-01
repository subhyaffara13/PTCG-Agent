
def test_canonical_ordering_AntiSymmetricTensor():
    v = symbols("v")

    c, d = symbols(('c','d'), above_fermi=True,
                                   cls=Dummy)
    k, l = symbols(('k','l'), below_fermi=True,
                                   cls=Dummy)

    # formerly, the left gave either the left or the right
    assert AntiSymmetricTensor(v, (k, l), (d, c)
        ) == -AntiSymmetricTensor(v, (l, k), (d, c))

