
def styler_multi(df_multi):
    return Styler(df_multi, uuid_len=0)


def styler_multi():
    df = DataFrame(
        data=np.arange(16).reshape(4, 4),
        columns=MultiIndex.from_product([["A", "B"], ["a", "b"]], names=["A&", "b&"]),
        index=MultiIndex.from_product([["X", "Y"], ["x", "y"]], names=["X>", "y_"]),
    )
    return Styler(df)

