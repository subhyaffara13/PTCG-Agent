
def test_geterr():
    err = sc.geterr()
    for key, value in err.items():
        assert_(key in _sf_error_code_map)
        assert_(value in _sf_error_actions)

