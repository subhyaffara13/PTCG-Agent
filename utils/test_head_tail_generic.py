
def test_head_tail_generic(index, frame_or_series):
    # GH#5370

    ndim = 2 if frame_or_series is DataFrame else 1
    shape = (len(index),) * ndim
    vals = np.random.default_rng(2).standard_normal(shape)
    obj = frame_or_series(vals, index=index)

    tm.assert_equal(obj.head(), obj.iloc[:5])
    tm.assert_equal(obj.tail(), obj.iloc[-5:])

    # 0-len
    tm.assert_equal(obj.head(0), obj.iloc[0:0])
    tm.assert_equal(obj.tail(0), obj.iloc[0:0])

    # bounded
    tm.assert_equal(obj.head(len(obj) + 1), obj)
    tm.assert_equal(obj.tail(len(obj) + 1), obj)

    # neg index
    tm.assert_equal(obj.head(-3), obj.head(len(index) - 3))
    tm.assert_equal(obj.tail(-3), obj.tail(len(index) - 3))

