
def test_multiindex_get_loc(request, lexsort_depth, keys, frame_fixture, cols):
    # GH7724, GH2646

    frame = request.getfixturevalue(frame_fixture)
    if lexsort_depth == 0:
        df = frame.copy(deep=False)
    else:
        df = frame.sort_values(by=cols[:lexsort_depth])

    mi = df.set_index(cols[:-1])
    assert not mi.index._lexsort_depth < lexsort_depth
    for key in keys:
        mask = np.ones(len(df), dtype=bool)

        # test for all partials of this key
        for i, k in enumerate(key):
            mask &= df.iloc[:, i] == k

            if not mask.any():
                assert key[: i + 1] not in mi.index
                continue

            assert key[: i + 1] in mi.index
            right = df[mask].copy(deep=False)

            if i + 1 != len(key):  # partial key
                return_value = right.drop(cols[: i + 1], axis=1, inplace=True)
                assert return_value is None
                return_value = right.set_index(cols[i + 1 : -1], inplace=True)
                assert return_value is None
                tm.assert_frame_equal(mi.loc[key[: i + 1]], right)

            else:  # full key
                return_value = right.set_index(cols[:-1], inplace=True)
                assert return_value is None
                if len(right) == 1:  # single hit
                    right = Series(
                        right["jolia"].values, name=right.index[0], index=["jolia"]
                    )
                    tm.assert_series_equal(mi.loc[key[: i + 1]], right)
                else:  # multi hit
                    tm.assert_frame_equal(mi.loc[key[: i + 1]], right)

