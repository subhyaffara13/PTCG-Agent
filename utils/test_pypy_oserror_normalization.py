
def test_pypy_oserror_normalization():
    # https://github.com/pybind/pybind11/issues/4075
    what = m.test_pypy_oserror_normalization()
    assert "this_filename_must_not_exist" in what

