
def test_map_box_timestamps():
    # GH 2689, GH 2627
    ser = Series(date_range("1/1/2000", periods=10))

    def func(x):
        return (x.hour, x.day, x.month)

    # it works!
    DataFrame(ser).map(func)

