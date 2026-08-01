
def test_non_categorical_value_label_name_conversion(temp_file):
    # Check conversion of invalid variable names
    data = DataFrame(
        {
            "invalid~!": [1, 1, 2, 3, 5, 8],  # Only alphanumeric and _
            "6_invalid": [1, 1, 2, 3, 5, 8],  # Must start with letter or _
            "invalid_name_longer_than_32_characters": [8, 8, 9, 9, 8, 8],  # Too long
            "aggregate": [2, 5, 5, 6, 6, 9],  # Reserved words
            (1, 2): [1, 2, 3, 4, 5, 6],  # Hashable non-string
        }
    )

    value_labels = {
        "invalid~!": {1: "label1", 2: "label2"},
        "6_invalid": {1: "label1", 2: "label2"},
        "invalid_name_longer_than_32_characters": {8: "eight", 9: "nine"},
        "aggregate": {5: "five"},
        (1, 2): {3: "three"},
    }

    expected = {
        "invalid__": {1: "label1", 2: "label2"},
        "_6_invalid": {1: "label1", 2: "label2"},
        "invalid_name_longer_than_32_char": {8: "eight", 9: "nine"},
        "_aggregate": {5: "five"},
        "_1__2_": {3: "three"},
    }

    msg = "Not all pandas column names were valid Stata variable names"
    with tm.assert_produces_warning(InvalidColumnName, match=msg):
        data.to_stata(temp_file, value_labels=value_labels)

    with StataReader(temp_file) as reader:
        reader_value_labels = reader.value_labels()
        assert reader_value_labels == expected

