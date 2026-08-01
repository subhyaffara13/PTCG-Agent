
def df_cross_compat():
    df = pd.DataFrame(
        {
            "a": list("abc"),
            "b": list(range(1, 4)),
            # 'c': np.arange(3, 6).astype('u1'),
            "d": np.arange(4.0, 7.0, dtype="float64"),
            "e": [True, False, True],
            "f": pd.date_range("20130101", periods=3),
            # 'g': pd.date_range('20130101', periods=3,
            #                    tz='US/Eastern'),
            # 'h': pd.date_range('20130101', periods=3, freq='ns')
        }
    )
    return df

