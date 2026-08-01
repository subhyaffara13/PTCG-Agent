
def test_td_constructor_on_nanoseconds(constructed_td, conversion):
    # GH#9273
    assert constructed_td == Timedelta(conversion)

