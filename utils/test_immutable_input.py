
def test_immutable_input(metric):
    if metric in ("jensenshannon", "mahalanobis", "seuclidean"):
        pytest.skip("not applicable")
    x = np.arange(10, dtype=np.float64)
    x.setflags(write=False)
    getattr(scipy.spatial.distance, metric)(x, x, w=x)

