
def test_infer_freq_range(periods, freq):
    freq = freq.upper()

    gen = date_range("1/1/2000", periods=periods, freq=freq)
    index = DatetimeIndex(gen.values)

    if not freq.startswith("QE-"):
        assert frequencies.infer_freq(index) == gen.freqstr
    else:
        inf_freq = frequencies.infer_freq(index)
        is_dec_range = inf_freq == "QE-DEC" and gen.freqstr in (
            "QE",
            "QE-DEC",
            "QE-SEP",
            "QE-JUN",
            "QE-MAR",
        )
        is_nov_range = inf_freq == "QE-NOV" and gen.freqstr in (
            "QE-NOV",
            "QE-AUG",
            "QE-MAY",
            "QE-FEB",
        )
        is_oct_range = inf_freq == "QE-OCT" and gen.freqstr in (
            "QE-OCT",
            "QE-JUL",
            "QE-APR",
            "QE-JAN",
        )
        assert is_dec_range or is_nov_range or is_oct_range

