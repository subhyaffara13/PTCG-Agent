
def _df_bar_subplot_checker(df_bar_data, df_bar_df, subplot_data_df, subplot_columns):
    subplot_sliced_by_source = [
        subplot_data_df.iloc[
            len(df_bar_data) * i : len(df_bar_data) * (i + 1)
        ].reset_index()
        for i in range(len(subplot_columns))
    ]

    if len(subplot_columns) == 1:
        expected_total_height = df_bar_df.loc[:, subplot_columns[0]]
    else:
        expected_total_height = df_bar_df.loc[:, subplot_columns].sum(axis=1)

    for i in range(len(subplot_columns)):
        sliced_df = subplot_sliced_by_source[i]
        if i == 0:
            # Checks that the bar chart starts y=0
            assert (sliced_df["y_coord"] == 0).all()
            height_iter = sliced_df["y_coord"].add(sliced_df["height"])
        else:
            height_iter = height_iter + sliced_df["height"]

        if i + 1 == len(subplot_columns):
            # Checks final height matches what is expected
            tm.assert_series_equal(
                height_iter, expected_total_height, check_names=False, check_dtype=False
            )
        else:
            # Checks each preceding bar ends where the next one starts
            next_start_coord = subplot_sliced_by_source[i + 1]["y_coord"]
            tm.assert_series_equal(
                height_iter, next_start_coord, check_names=False, check_dtype=False
            )

