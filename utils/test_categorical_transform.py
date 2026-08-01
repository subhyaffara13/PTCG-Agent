
def test_categorical_transform():
    # GH 29037
    df = DataFrame(
        {
            "package_id": [1, 1, 1, 2, 2, 3],
            "status": [
                "Waiting",
                "OnTheWay",
                "Delivered",
                "Waiting",
                "OnTheWay",
                "Waiting",
            ],
        }
    )

    delivery_status_type = pd.CategoricalDtype(
        categories=["Waiting", "OnTheWay", "Delivered"], ordered=True
    )
    df["status"] = df["status"].astype(delivery_status_type)
    df["last_status"] = df.groupby("package_id")["status"].transform(max)
    result = df.copy()

    expected = DataFrame(
        {
            "package_id": [1, 1, 1, 2, 2, 3],
            "status": [
                "Waiting",
                "OnTheWay",
                "Delivered",
                "Waiting",
                "OnTheWay",
                "Waiting",
            ],
            "last_status": [
                "Waiting",
                "Waiting",
                "Waiting",
                "Waiting",
                "Waiting",
                "Waiting",
            ],
        }
    )

    expected["status"] = expected["status"].astype(delivery_status_type)
    tm.assert_frame_equal(result, expected)


def test_categorical_transform():
    # GH#36327
    values = np.random.default_rng(2).choice([1, 2, None], 30)
    df = pd.DataFrame(
        {"x": pd.Categorical(values, categories=[1, 2, 3]), "y": range(len(values))}
    )
    gb = df.groupby("x", dropna=False, observed=False)
    result = gb.transform(lambda x: x.sum())
    expected = gb.transform("sum")
    tm.assert_frame_equal(result, expected)

