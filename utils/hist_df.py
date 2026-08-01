
def hist_df():
    n = 50
    rng = np.random.default_rng(10)
    gender = rng.choice(["Male", "Female"], size=n)
    classroom = rng.choice(["A", "B", "C"], size=n)

    hist_df = DataFrame(
        {
            "gender": gender,
            "classroom": classroom,
            "height": rng.normal(66, 4, size=n),
            "weight": rng.normal(161, 32, size=n),
            "category": rng.integers(4, size=n),
            "datetime": to_datetime(
                rng.integers(
                    812419200000000000,
                    819331200000000000,
                    size=n,
                    dtype=np.int64,
                )
            ),
        }
    )
    return hist_df


def hist_df():
    df = DataFrame(
        np.random.default_rng(2).standard_normal((30, 2)), columns=["A", "B"]
    )
    df["C"] = np.random.default_rng(2).choice(["a", "b", "c"], 30)
    df["D"] = np.random.default_rng(2).choice(["a", "b", "c"], 30)
    return df

