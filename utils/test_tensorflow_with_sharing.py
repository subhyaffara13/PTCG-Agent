
def test_tensorflow_with_sharing(string: str) -> None:
    np = pytest.importorskip("numpy")
    tf = pytest.importorskip("tensorflow")

    views = build_views(string)
    ein = contract(string, *views, optimize=False, use_blas=False)

    shps = [v.shape for v in views]
    expr = contract_expression(string, *shps, optimize=True)

    sess = TFSession(config=_TF_CONFIG)

    with sess.as_default(), sharing.shared_intermediates() as cache:
        tfl1 = expr(*views, backend="tensorflow")
        assert sharing.get_sharing_cache() is cache
        cache_sz = len(cache)
        assert cache_sz > 0
        tfl2 = expr(*views, backend="tensorflow")
        assert len(cache) == cache_sz

    assert all(isinstance(t, tf.Tensor) for t in cache.values())

    assert np.allclose(ein, tfl1)
    assert np.allclose(ein, tfl2)

