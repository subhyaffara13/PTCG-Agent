
def test_infer_freq_non_nano():
    arr = np.arange(10).astype(np.int64).view("M8[s]")
    dta = DatetimeArray._simple_new(arr, dtype=arr.dtype)
    res = frequencies.infer_freq(dta)
    assert res == "s"

    arr2 = arr.view("m8[ms]")
    tda = TimedeltaArray._simple_new(arr2, dtype=arr2.dtype)
    res2 = frequencies.infer_freq(tda)
    assert res2 == "ms"

