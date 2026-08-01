
def test_isoformat(td, expected_iso):
    assert td.isoformat() == expected_iso


def test_isoformat(ts, timespec, expected_iso):
    assert ts.isoformat(timespec=timespec) == expected_iso

