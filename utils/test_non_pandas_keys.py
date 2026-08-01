
def test_non_pandas_keys(temp_h5_path):
    class Table1(tables.IsDescription):
        value1 = tables.Float32Col()

    class Table2(tables.IsDescription):
        value2 = tables.Float32Col()

    class Table3(tables.IsDescription):
        value3 = tables.Float32Col()

    with tables.open_file(temp_h5_path, mode="w") as h5file:
        group = h5file.create_group("/", "group")
        h5file.create_table(group, "table1", Table1, "Table 1")
        h5file.create_table(group, "table2", Table2, "Table 2")
        h5file.create_table(group, "table3", Table3, "Table 3")
    with HDFStore(temp_h5_path) as store:
        assert len(store.keys(include="native")) == 3
        expected = {"/group/table1", "/group/table2", "/group/table3"}
        assert set(store.keys(include="native")) == expected
        assert set(store.keys(include="pandas")) == set()
        for name in expected:
            df = store.get(name)
            assert len(df.columns) == 1

