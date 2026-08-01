
def test_numpy_linalg():
    bad_results = check_dir(np.linalg)
    assert bad_results == {}

