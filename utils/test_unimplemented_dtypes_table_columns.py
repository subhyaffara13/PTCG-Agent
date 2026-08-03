import re

def test_unimplemented_dtypes_table_columns(temp_hdfstore):
    dtypes = [("date", datetime.date(2001, 1, 2))]

    # currently not supported dtypes ####
    for n, f in dtypes:
        df = DataFrame(
            1.1 * np.arange(120).reshape((30, 4)),
            columns=Index(list("ABCD"), dtype=object),
            index=Index([f"i-{i}" for i in range(30)], dtype=object),
        )
        df[n] = f
        msg = re.escape(f"[{n}] is not implemented as a table column")
        with pytest.raises(TypeError, match=msg):
            temp_hdfstore.append(f"df1_{n}", df)

