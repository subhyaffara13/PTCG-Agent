
def test_cummax_i8_at_implementation_bound():
    # the minimum value used to be treated as NPY_NAT+1 instead of NPY_NAT
    #  for int64 dtype GH#46382
    ser = Series([pd.NaT._value + n for n in range(5)])
    df = DataFrame({"A": 1, "B": ser, "C": ser._values.view("M8[ns]")})
    gb = df.groupby("A")

    res = gb.cummax()
    exp = df[["B", "C"]]
    tm.assert_frame_equal(res, exp)

