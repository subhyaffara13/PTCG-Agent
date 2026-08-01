
def test_numba_not_installed_option_context():
    with pytest.raises(ImportError, match="`Import numba` failed"):
        with option_context("compute.use_numba", True):
            pass

