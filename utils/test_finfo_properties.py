
def test_finfo_properties(dtype, ma_fixture, prop, request):
    """Test that finfo properties match expected machine arithmetic values."""
    ma = request.getfixturevalue(ma_fixture)
    finfo = np.finfo(dtype)

    actual = getattr(finfo, prop)
    expected = getattr(ma, prop)

    assert actual == expected, (
        f"finfo({dtype}) property '{prop}' mismatch: "
        f"expected {expected}, got {actual}"
    )

