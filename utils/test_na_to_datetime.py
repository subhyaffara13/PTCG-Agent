
def test_na_to_datetime(nulls_fixture, klass):
    if isinstance(nulls_fixture, Decimal):
        with pytest.raises(TypeError, match="not convertible to datetime"):
            to_datetime(klass([nulls_fixture]))

    else:
        result = to_datetime(klass([nulls_fixture]))

        assert result[0] is NaT

