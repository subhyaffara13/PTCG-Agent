
def test_convert_datetime64_to_datetimestruct(install_temp):
    # GH#21199
    import checks

    res = checks.convert_datetime64_to_datetimestruct()

    exp = {
        "year": 2022,
        "month": 3,
        "day": 15,
        "hour": 20,
        "min": 1,
        "sec": 55,
        "us": 260292,
        "ps": 0,
        "as": 0,
    }

    assert res == exp

