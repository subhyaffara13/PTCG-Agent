
def test_iso_constructor_raises(fmt):
    msg = f"Invalid ISO 8601 Duration format - {fmt}"
    with pytest.raises(ValueError, match=msg):
        Timedelta(fmt)

