import os

def test_ckdtree_parallel(kdtree_type, monkeypatch):
    # check if parallel=True also generates correct query results
    np.random.seed(0)
    n = 5000
    k = 4
    points = np.random.randn(n, k)
    T = kdtree_type(points)
    T1 = T.query(points, k=5, workers=64)[-1]
    T2 = T.query(points, k=5, workers=-1)[-1]
    T3 = T.query(points, k=5)[-1]
    assert_array_equal(T1, T2)
    assert_array_equal(T1, T3)

    monkeypatch.setattr(os, 'cpu_count', lambda: None)
    with pytest.raises(NotImplementedError, match="Cannot determine the"):
        T.query(points, 1, workers=-1)

