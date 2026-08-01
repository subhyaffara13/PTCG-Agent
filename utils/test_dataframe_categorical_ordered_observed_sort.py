
def test_dataframe_categorical_ordered_observed_sort(ordered, observed, sort):
    # GH 25871: Fix groupby sorting on ordered Categoricals
    # GH 25167: Groupby with observed=True doesn't sort

    # Build a dataframe with cat having one unobserved category ('missing'),
    # and a Series with identical values
    label = Categorical(
        ["d", "a", "b", "a", "d", "b"],
        categories=["a", "b", "missing", "d"],
        ordered=ordered,
    )
    val = Series(["d", "a", "b", "a", "d", "b"])
    df = DataFrame({"label": label, "val": val})

    # aggregate on the Categorical
    result = df.groupby("label", observed=observed, sort=sort)["val"].aggregate("first")

    # If ordering works, we expect index labels equal to aggregation results,
    # except for 'observed=False': label 'missing' has aggregation None
    label = Series(result.index.array, dtype="object")
    aggr = Series(result.array)
    if not observed:
        aggr[aggr.isna()] = "missing"
    if not all(label == aggr):
        msg = (
            "Labels and aggregation results not consistently sorted\n"
            f"for (ordered={ordered}, observed={observed}, sort={sort})\n"
            f"Result:\n{result}"
        )
        pytest.fail(msg)

