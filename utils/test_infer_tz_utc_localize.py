
def test_infer_tz_utc_localize(infer_setup):
    _, _, start, end, start_naive, end_naive = infer_setup
    utc = timezone.utc

    start = start_naive.astimezone(utc)
    end = end_naive.astimezone(utc)

    assert timezones.infer_tzinfo(start, end) is utc

