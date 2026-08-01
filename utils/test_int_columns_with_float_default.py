
def test_int_columns_with_float_default():
    # https://github.com/pandas-dev/pandas/pull/60694
    df = DataFrame(
        {
            3: [1, 0, 0],
            4: [0, 1, 0],
        },
    )
    with pytest.raises(ValueError, match="Trying to coerce float values to integers"):
        from_dummies(df, default_category=0.5)

