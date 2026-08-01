
def test_get_to_timestamp_base(freqstr, exp_freqstr):
    off = to_offset(freqstr)
    per = Period._from_ordinal(1, off)
    exp_code = to_offset(exp_freqstr)._period_dtype_code

    result_code = per._dtype._get_to_timestamp_base()
    assert result_code == exp_code

