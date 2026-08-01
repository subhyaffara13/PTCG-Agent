
def test_select_categorical_string_columns(temp_hdfstore, model):
    # Corresponding to BUG: 57608

    models = CategoricalDtype(categories=["name", "longname", "verylongname"])
    df = DataFrame(
        {"modelId": ["name", "longname", "longname"], "value": [1, 2, 3]}
    ).astype({"modelId": models, "value": int})

    temp_hdfstore.append("df", df, data_columns=["modelId"])

    result = temp_hdfstore.select("df", "modelId == model")
    expected = df[df["modelId"] == model]
    tm.assert_frame_equal(result, expected)

