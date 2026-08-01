
def test_at_timezone():
    # https://github.com/pandas-dev/pandas/issues/33544
    result = DataFrame({"foo": [datetime(2000, 1, 1)]})
    with pytest.raises(TypeError, match="Invalid value"):
        result.at[0, "foo"] = datetime(2000, 1, 2, tzinfo=timezone.utc)

