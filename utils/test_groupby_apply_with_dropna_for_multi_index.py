
def test_groupby_apply_with_dropna_for_multi_index(dropna, data, selected_data, levels):
    # GH 35889

    df = pd.DataFrame(data)
    gb = df.groupby("groups", dropna=dropna)
    result = gb.apply(lambda grp: pd.DataFrame({"values": range(len(grp))}))

    mi_tuples = tuple(zip(data["groups"], selected_data["values"], strict=False))
    mi = pd.MultiIndex.from_tuples(mi_tuples, names=["groups", None])
    # Since right now, by default MI will drop NA from levels when we create MI
    # via `from_*`, so we need to add NA for level manually afterwards.
    if not dropna and levels:
        mi = mi.set_levels(levels, level="groups")

    expected = pd.DataFrame(selected_data, index=mi)
    tm.assert_frame_equal(result, expected)

