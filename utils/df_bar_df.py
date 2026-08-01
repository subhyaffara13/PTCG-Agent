
def df_bar_df(df_bar_data) -> DataFrame:
    df_bar_df = DataFrame(
        {
            "A": df_bar_data,
            "B": df_bar_data[::-1],
            "C": df_bar_data[0],
            "D": df_bar_data[-1],
        }
    )
    return df_bar_df

