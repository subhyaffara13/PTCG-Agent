
def test_reindex_limit_arg_with_multiindex():
    # GH21247

    idx = MultiIndex.from_tuples([(3, "A"), (4, "A"), (4, "B")])

    df = pd.Series([0.02, 0.01, 0.012], index=idx)

    new_idx = MultiIndex.from_tuples(
        [
            (3, "A"),
            (3, "B"),
            (4, "A"),
            (4, "B"),
            (4, "C"),
            (5, "B"),
            (5, "C"),
            (6, "B"),
            (6, "C"),
        ]
    )

    with pytest.raises(
        ValueError,
        match="limit argument only valid if doing pad, backfill or nearest reindexing",
    ):
        df.reindex(new_idx, fill_value=0, limit=1)

