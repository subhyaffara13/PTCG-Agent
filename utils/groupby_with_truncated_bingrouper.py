
def groupby_with_truncated_bingrouper(frame_for_truncated_bingrouper):
    """
    GroupBy object such that gb._grouper is a BinGrouper and
    len(gb._grouper.result_index) < len(gb._grouper.group_keys_seq)

    Aggregations on this groupby should have

        dti = date_range("2013-09-01", "2013-10-01", freq="5D", name="Date")

    As either the index or an index level.
    """
    df = frame_for_truncated_bingrouper

    tdg = Grouper(key="Date", freq="5D")
    gb = df.groupby(tdg)

    # check we're testing the case we're interested in
    assert len(gb._grouper.result_index) != len(gb._grouper.codes)

    return gb

