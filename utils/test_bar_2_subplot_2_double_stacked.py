
def test_bar_2_subplot_2_double_stacked(df_bar_data, df_bar_df, subplot_division):
    ax = df_bar_df.plot(subplots=subplot_division, kind="bar", stacked=True)
    subplot_data_df_list = _df_bar_xyheight_from_ax_helper(
        df_bar_data, ax, subplot_division
    )
    for i in range(len(subplot_data_df_list)):
        _df_bar_subplot_checker(
            df_bar_data, df_bar_df, subplot_data_df_list[i], subplot_division[i]
        )

