
def test_non_space_filler():
    # From Thomas Kluyver:
    #
    # Apparently, some non-space filler characters can be seen, this is
    # supported by specifying the 'delimiter' character:
    #
    # http://publib.boulder.ibm.com/infocenter/dmndhelp/v6r1mx/index.jsp?topic=/com.ibm.wbit.612.help.config.doc/topics/rfixwidth.html
    data = """\
A~~~~B~~~~C~~~~~~~~~~~~D~~~~~~~~~~~~E
201158~~~~360.242940~~~149.910199~~~11950.7
201159~~~~444.953632~~~166.985655~~~11788.4
201160~~~~364.136849~~~183.628767~~~11806.2
201161~~~~413.836124~~~184.375703~~~11916.8
201162~~~~502.953953~~~173.237159~~~12468.3
"""
    colspecs = [(0, 4), (4, 8), (8, 20), (21, 33), (34, 43)]
    result = read_fwf(StringIO(data), colspecs=colspecs, delimiter="~")

    expected = DataFrame(
        [
            [2011, 58, 360.242940, 149.910199, 11950.7],
            [2011, 59, 444.953632, 166.985655, 11788.4],
            [2011, 60, 364.136849, 183.628767, 11806.2],
            [2011, 61, 413.836124, 184.375703, 11916.8],
            [2011, 62, 502.953953, 173.237159, 12468.3],
        ],
        columns=["A", "B", "C", "D", "E"],
    )
    tm.assert_frame_equal(result, expected)

