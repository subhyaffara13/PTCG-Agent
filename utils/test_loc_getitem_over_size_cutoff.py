
def test_loc_getitem_over_size_cutoff(monkeypatch):
    # #1821

    monkeypatch.setattr(libindex, "_SIZE_CUTOFF", 1000)

    # create large list of non periodic datetime
    dates = []
    sec = timedelta(seconds=1)
    half_sec = timedelta(microseconds=500000)
    d = datetime(2011, 12, 5, 20, 30)
    n = 1100
    for i in range(n):
        dates.append(d)
        dates.append(d + sec)
        dates.append(d + sec + half_sec)
        dates.append(d + sec + sec + half_sec)
        d += 3 * sec

    # duplicate some values in the list
    duplicate_positions = np.random.default_rng(2).integers(0, len(dates) - 1, 20)
    for p in duplicate_positions:
        dates[p + 1] = dates[p]

    df = DataFrame(
        np.random.default_rng(2).standard_normal((len(dates), 4)),
        index=dates,
        columns=list("ABCD"),
    )

    pos = n * 3
    timestamp = df.index[pos]
    assert timestamp in df.index

    # it works!
    df.loc[timestamp]
    assert len(df.loc[[timestamp]]) > 0

