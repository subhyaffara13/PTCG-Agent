
def groupy_test_df():
    return DataFrame(
        {"price": [10, 11, 9], "volume": [50, 60, 50]},
        index=date_range("01/01/2018", periods=3, freq="W", unit="ns"),
    )

