
def test_temp_setattr(with_exception):
    # GH#45954
    ser = Series(dtype=object)
    ser.name = "first"
    # Raise a ValueError in either case to satisfy pytest.raises
    match = "Inside exception raised" if with_exception else "Outside exception raised"
    with pytest.raises(ValueError, match=match):
        with com.temp_setattr(ser, "name", "second"):
            assert ser.name == "second"
            if with_exception:
                raise ValueError("Inside exception raised")
        raise ValueError("Outside exception raised")
    assert ser.name == "first"

