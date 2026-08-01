
def test_timedelta_new_npnat():
    # GH#48898
    nat = np.timedelta64("NaT", "h")
    assert Timedelta(nat) is NaT

