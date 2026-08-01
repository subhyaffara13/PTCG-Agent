
def test_vmin_vmax_widening(df_pos, df_neg, df_mix, values, vmin, vmax, nullify, align):
    # test that widening occurs if any vmax > data_values or vmin < data_values
    if align == "mid":  # mid acts as left or right in each case
        if values == "positive":
            align = "left"
        elif values == "negative":
            align = "right"
    df = {"positive": df_pos, "negative": df_neg, "mixed": df_mix}[values]
    vmin = None if nullify == "vmin" else vmin
    vmax = None if nullify == "vmax" else vmax

    expand_df = df.copy()
    expand_df.loc[3, :], expand_df.loc[4, :] = vmin, vmax

    result = (
        df.style.bar(align=align, vmin=vmin, vmax=vmax, color=["red", "green"])
        ._compute()
        .ctx
    )
    expected = expand_df.style.bar(align=align, color=["red", "green"])._compute().ctx
    assert result.items() <= expected.items()

