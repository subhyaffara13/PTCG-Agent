
def test_yen_no_paths():
    distances = yen(
        directed_G,
        source=2,
        sink=3,
        K=1,
    )
    assert distances.size == 0

