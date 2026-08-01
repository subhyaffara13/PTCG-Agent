
def test_under_specified():
    data = """\
A   B     C            D            E
201158    360.242940   149.910199   11950.7
201159    444.953632   166.985655   11788.4
201160    364.136849   183.628767   11806.2
201161    413.836124   184.375703   11916.8
201162    502.953953   173.237159   12468.3
"""
    with pytest.raises(ValueError, match="Must specify either"):
        read_fwf(StringIO(data), colspecs=None, widths=None)

