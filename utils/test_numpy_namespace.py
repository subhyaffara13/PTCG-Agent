
def test_numpy_namespace():
    # We override dir to not show these members
    allowlist = {
        'recarray': 'numpy.rec.recarray',
    }
    bad_results = check_dir(np)
    # pytest gives better error messages with the builtin assert than with
    # assert_equal
    assert bad_results == allowlist

