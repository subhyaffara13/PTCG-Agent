import re

def test_table_index_incompatible_dtypes(temp_hdfstore):
    df1 = DataFrame({"a": [1, 2, 3]})
    df2 = DataFrame(
        {"a": [4, 5, 6]}, index=date_range("1/1/2000", periods=3, unit="ns")
    )

    temp_hdfstore.put("frame", df1, format="table")
    msg = re.escape("incompatible kind in col [integer - datetime64[ns]]")
    with pytest.raises(TypeError, match=msg):
        temp_hdfstore.put("frame", df2, format="table", append=True)

