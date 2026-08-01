
def test_is_unique(data, expected):
    # GH#11946 / GH#25180
    ser = Series(data)
    assert ser.is_unique is expected

