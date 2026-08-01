
def test_kdtree_box_0boxsize(kdtree_type):
    # check ckdtree periodic boundary that mimics non-periodic
    n = 2000
    m = 2
    k = 3
    np.random.seed(1234)
    data = np.random.uniform(size=(n, m))
    kdtree = kdtree_type(data, leafsize=1, boxsize=0.0)

    # use the standard python KDTree for the simulated periodic box
    kdtree2 = kdtree_type(data, leafsize=1)

    for p in [1, 2, np.inf]:
        dd, ii = kdtree.query(data, k, p=p)

        dd1, ii1 = kdtree2.query(data, k, p=p)
        assert_almost_equal(dd, dd1)
        assert_equal(ii, ii1)

