
def regular():
    return DataFrame(
        {"A": date_range("20130101", periods=5, freq="s"), "B": range(5)}
    ).set_index("A")

