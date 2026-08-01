
def test_td_from_repr_roundtrip(val):
    # round-trip both for string and value
    td = Timedelta(val)
    assert Timedelta(td.value) == td

    assert Timedelta(str(td)) == td
    assert Timedelta(td._repr_base(format="all")) == td
    assert Timedelta(td._repr_base()) == td

