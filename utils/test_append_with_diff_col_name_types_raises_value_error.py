import re

def test_append_with_diff_col_name_types_raises_value_error(temp_hdfstore):
    df = DataFrame(np.random.default_rng(2).standard_normal((10, 1)))
    df2 = DataFrame({"a": np.random.default_rng(2).standard_normal(10)})
    df3 = DataFrame({(1, 2): np.random.default_rng(2).standard_normal(10)})
    df4 = DataFrame({("1", 2): np.random.default_rng(2).standard_normal(10)})
    df5 = DataFrame({("1", 2, object): np.random.default_rng(2).standard_normal(10)})

    name = "df_diff_valerror"
    temp_hdfstore.append(name, df)

    for d in (df2, df3, df4, df5):
        msg = re.escape(
            "cannot match existing table structure for [0] on appending data"
        )
        with pytest.raises(ValueError, match=msg):
            temp_hdfstore.append(name, d)

