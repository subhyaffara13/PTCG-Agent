
def test_is_timedelta64_object(install_temp):
    import checks

    with pytest.warns(
        DeprecationWarning,
        match="The 'generic' unit for NumPy timedelta is deprecated",
    ):
        assert checks.is_td64(np.timedelta64(1234))

    assert checks.is_td64(np.timedelta64(1234, "ns"))
    assert checks.is_td64(np.timedelta64("NaT", "ns"))

    assert not checks.is_td64(1)
    assert not checks.is_td64(None)
    assert not checks.is_td64("foo")
    assert not checks.is_td64(np.datetime64("now", "s"))

