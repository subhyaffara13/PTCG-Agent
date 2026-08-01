
def test_select_iterator_non_complete_8014_empty_where(temp_hdfstore):
    chunksize = 1e4
    expected = DataFrame(
        np.random.default_rng(2).standard_normal((100064, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=100064, freq="s", unit="ns"),
    )
    temp_hdfstore.append("df", expected)

    end_dt = expected.index[-1]

    # select w/iterator and where clause, single term, begin of range
    where = f"index > '{end_dt}'"
    results = list(temp_hdfstore.select("df", where=where, chunksize=chunksize))
    assert 0 == len(results)

