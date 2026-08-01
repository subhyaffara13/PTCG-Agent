
def test_non_categorical_value_label_convert_categoricals_error(temp_file):
    # Mapping more than one value to the same label is valid for Stata
    # labels, but can't be read with convert_categoricals=True
    value_labels = {
        "repeated_labels": {10: "Ten", 20: "More than ten", 40: "More than ten"}
    }

    data = DataFrame(
        {
            "repeated_labels": [10, 10, 20, 20, 40, 40],
        }
    )

    data.to_stata(temp_file, value_labels=value_labels)

    with StataReader(temp_file, convert_categoricals=False) as reader:
        reader_value_labels = reader.value_labels()
    assert reader_value_labels == value_labels

    col = "repeated_labels"
    repeats = "-" * 80 + "\n" + "\n".join(["More than ten"])

    msg = f"""
Value labels for column {col} are not unique. These cannot be converted to
pandas categoricals.

Either read the file with `convert_categoricals` set to False or use the
low level interface in `StataReader` to separately read the values and the
value_labels.

The repeated labels are:
{repeats}
"""
    with pytest.raises(ValueError, match=msg):
        read_stata(temp_file, convert_categoricals=True)

