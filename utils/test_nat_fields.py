
def test_nat_fields(nat, idx):
    for field in idx._field_ops:
        # weekday is a property of DTI, but a method
        # on NaT/Timestamp for compat with datetime
        if field == "weekday":
            continue

        result = getattr(NaT, field)
        assert np.isnan(result)

        result = getattr(nat, field)
        assert np.isnan(result)

    for field in idx._bool_ops:
        result = getattr(NaT, field)
        assert result is False

        result = getattr(nat, field)
        assert result is False

