
def test_frame_map_dont_convert_datetime64(unit):
    dtype = f"M8[{unit}]"
    df = DataFrame({"x1": [datetime(1996, 1, 1)]}, dtype=dtype)

    df = df.map(lambda x: x + BDay())
    df = df.map(lambda x: x + BDay())

    result = df.x1.dtype
    assert result == dtype

