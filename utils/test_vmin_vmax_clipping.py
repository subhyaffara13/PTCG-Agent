
def test_vmin_vmax_clipping(df_pos, df_neg, df_mix, values, vmin, vmax, nullify, align):
    # test that clipping occurs if any vmin > data_values or vmax < data_values
    if align == "mid":  # mid acts as left or right in each case
        if values == "positive":
            align = "left"
        elif values == "negative":
            align = "right"
    df = {"positive": df_pos, "negative": df_neg, "mixed": df_mix}[values]
    vmin = None if nullify == "vmin" else vmin
    vmax = None if nullify == "vmax" else vmax

    clip_df = df.where(df <= (vmax if vmax else 999), other=vmax)
    clip_df = clip_df.where(clip_df >= (vmin if vmin else -999), other=vmin)

    result = (
        df.style.bar(align=align, vmin=vmin, vmax=vmax, color=["red", "green"])
        ._compute()
        .ctx
    )
    expected = clip_df.style.bar(align=align, color=["red", "green"])._compute().ctx
    assert result == expected

