
def seed_df(seed_nans, n, m):
    days = date_range("2015-08-24", periods=10)

    frame = DataFrame(
        {
            "1st": np.random.default_rng(2).choice(list("abcd"), n),
            "2nd": np.random.default_rng(2).choice(days, n),
            "3rd": np.random.default_rng(2).integers(1, m + 1, n),
        }
    )

    if seed_nans:
        # Explicitly cast to float to avoid implicit cast when setting nan
        frame["3rd"] = frame["3rd"].astype("float")
        frame.loc[1::11, "1st"] = np.nan
        frame.loc[3::17, "2nd"] = np.nan
        frame.loc[7::19, "3rd"] = np.nan
        frame.loc[8::19, "3rd"] = np.nan
        frame.loc[9::19, "3rd"] = np.nan

    return frame

