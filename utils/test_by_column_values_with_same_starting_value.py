
def test_by_column_values_with_same_starting_value(any_string_dtype):
    # GH29635
    dtype = any_string_dtype
    df = DataFrame(
        {
            "Name": ["Thomas", "Thomas", "Thomas John"],
            "Credit": [1200, 1300, 900],
            "Mood": Series(["sad", "happy", "happy"], dtype=dtype),
        }
    )
    aggregate_details = {"Mood": Series.mode, "Credit": "sum"}

    result = df.groupby(["Name"]).agg(aggregate_details)
    expected = DataFrame(
        {
            "Mood": [["happy", "sad"], "happy"],
            "Credit": [2500, 900],
            "Name": ["Thomas", "Thomas John"],
        },
    ).set_index("Name")
    if getattr(dtype, "storage", None) == "pyarrow":
        mood_values = pd.array(["happy", "sad"], dtype=dtype)
        expected["Mood"] = [mood_values, "happy"]
    tm.assert_frame_equal(result, expected)

