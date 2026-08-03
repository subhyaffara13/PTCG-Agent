import re

def test_unimplemented_dtypes_table_columns2(temp_hdfstore):
    # frame
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=Index([f"i-{i}" for i in range(30)], dtype=object),
    )
    df["obj1"] = "foo"
    df["obj2"] = "bar"
    df["datetime1"] = datetime.date(2001, 1, 2)
    df = df._consolidate()

    # this fails because we have a date in the object block......
    msg = "|".join(
        [
            re.escape(
                "Cannot serialize the column [datetime1]\nbecause its data "
                "contents are not [string] but [date] object dtype"
            ),
            re.escape("[date] is not implemented as a table column"),
        ]
    )
    with pytest.raises(TypeError, match=msg):
        temp_hdfstore.append("df_unimplemented", df)

