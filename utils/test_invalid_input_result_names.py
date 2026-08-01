
def test_invalid_input_result_names(result_names):
    # GH 44354
    df1 = pd.DataFrame(
        {"col1": ["a", "b", "c"], "col2": [1.0, 2.0, np.nan], "col3": [1.0, 2.0, 3.0]},
    )
    df2 = pd.DataFrame(
        {
            "col1": ["c", "b", "c"],
            "col2": [1.0, 2.0, np.nan],
            "col3": [1.0, 2.0, np.nan],
        },
    )
    with pytest.raises(
        TypeError,
        match=(
            f"Passing 'result_names' as a {type(result_names)} is not "
            "supported. Provide 'result_names' as a tuple instead."
        ),
    ):
        df1.compare(df2, result_names=result_names)

