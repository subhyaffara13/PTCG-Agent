
def test_broken_barh_align():
    fig, ax = plt.subplots()
    pc = ax.broken_barh([(0, 10)], (0, 2))
    for path in pc.get_paths():
        assert_array_equal(path.get_extents().intervaly, [0, 2])

    pc = ax.broken_barh([(0, 10)], (10, 2), align="center")
    for path in pc.get_paths():
        assert_array_equal(path.get_extents().intervaly, [9, 11])

    pc = ax.broken_barh([(0, 10)], (20, 2), align="top")
    for path in pc.get_paths():
        assert_array_equal(path.get_extents().intervaly, [18, 20])

