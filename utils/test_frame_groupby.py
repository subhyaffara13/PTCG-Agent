
def test_frame_groupby(tsframe):
    grouped = tsframe.groupby(lambda x: x.weekday())

    # aggregate
    aggregated = grouped.aggregate("mean")
    assert len(aggregated) == 5
    assert len(aggregated.columns) == 4

    # by string
    tscopy = tsframe.copy()
    tscopy["weekday"] = [x.weekday() for x in tscopy.index]
    stragged = tscopy.groupby("weekday").aggregate("mean")
    tm.assert_frame_equal(stragged, aggregated, check_names=False)

    # transform
    grouped = tsframe.head(30).groupby(lambda x: x.weekday())
    transformed = grouped.transform(lambda x: x - x.mean())
    assert len(transformed) == 30
    assert len(transformed.columns) == 4

    # transform propagate
    transformed = grouped.transform(lambda x: x.mean())
    for name, group in grouped:
        mean = group.mean()
        for idx in group.index:
            tm.assert_series_equal(transformed.xs(idx), mean, check_names=False)

    # iterate
    for weekday, group in grouped:
        assert group.index[0].weekday() == weekday

    # groups / group_indices
    groups = grouped.groups
    indices = grouped.indices

    for k, v in groups.items():
        samething = tsframe.index.take(indices[k])
        assert (samething == v).all()

