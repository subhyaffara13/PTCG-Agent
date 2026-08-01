
def test_to_offset_pd_timedelta(kwargs, expected):
    # see gh-9064
    td = Timedelta(**kwargs)
    result = to_offset(td)
    assert result == expected

