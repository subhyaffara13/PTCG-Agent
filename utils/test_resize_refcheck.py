
def test_resize_refcheck(install_temp):
    import checks
    msg = "It is possible that this is a false positive."
    with pytest.raises(ValueError, match=msg):
        checks.resize_refcheck_test()

