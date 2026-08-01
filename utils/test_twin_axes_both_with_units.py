
def test_twin_axes_both_with_units():
    host = host_subplot(111)
    host.yaxis.axis_date()
    host.plot([0, 1, 2], [0, 1, 2])
    twin = host.twinx()
    twin.plot(["a", "b", "c"])
    assert host.get_yticklabels()[0].get_text() == "00:00:00"
    assert twin.get_yticklabels()[0].get_text() == "a"

