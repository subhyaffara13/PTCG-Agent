
def test_is_datetime64_object(install_temp):
    import checks

    assert checks.is_dt64(np.datetime64(1234, "ns"))
    assert checks.is_dt64(np.datetime64("NaT", "ns"))

    assert not checks.is_dt64(1)
    assert not checks.is_dt64(None)
    assert not checks.is_dt64("foo")

    with pytest.warns(
        DeprecationWarning,
        match="The 'generic' unit for NumPy timedelta is deprecated",
    ):
        assert not checks.is_dt64(np.timedelta64(1234))

