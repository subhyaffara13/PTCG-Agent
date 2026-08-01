
def test_large_multiindex_error(monkeypatch):
    # GH12527
    size_cutoff = 50
    with monkeypatch.context() as m:
        m.setattr(libindex, "_SIZE_CUTOFF", size_cutoff)
        df_below_cutoff = pd.DataFrame(
            1,
            index=MultiIndex.from_product([[1, 2], range(size_cutoff - 1)]),
            columns=["dest"],
        )
        with pytest.raises(KeyError, match=r"^\(-1, 0\)$"):
            df_below_cutoff.loc[(-1, 0), "dest"]
        with pytest.raises(KeyError, match=r"^\(3, 0\)$"):
            df_below_cutoff.loc[(3, 0), "dest"]
        df_above_cutoff = pd.DataFrame(
            1,
            index=MultiIndex.from_product([[1, 2], range(size_cutoff + 1)]),
            columns=["dest"],
        )
        with pytest.raises(KeyError, match=r"^\(-1, 0\)$"):
            df_above_cutoff.loc[(-1, 0), "dest"]
        with pytest.raises(KeyError, match=r"^\(3, 0\)$"):
            df_above_cutoff.loc[(3, 0), "dest"]

