
def test_align_mixed_cases(df_mix, align, exp, nans):
    # test different align cases for mixed positive and negative values
    # also test no impact of NaNs and no_bar
    expected = {(0, 0): exp[0], (1, 0): exp[1], (2, 0): exp[2]}
    if nans:
        df_mix.loc[3, :] = np.nan
        expected.update({(3, 0): no_bar()})
    result = df_mix.style.bar(align=align)._compute().ctx
    assert result == expected

