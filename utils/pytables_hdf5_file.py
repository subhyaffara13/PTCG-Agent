
def pytables_hdf5_file(temp_h5_path):
    """
    Use PyTables to create a simple HDF5 file.
    """
    table_schema = {
        "c0": tables.Time64Col(pos=0),
        "c1": tables.StringCol(5, pos=1),
        "c2": tables.Int64Col(pos=2),
    }

    t0 = 1_561_105_000.0

    testsamples = [
        {"c0": t0, "c1": "aaaaa", "c2": 1},
        {"c0": t0 + 1, "c1": "bbbbb", "c2": 2},
        {"c0": t0 + 2, "c1": "ccccc", "c2": 10**5},
        {"c0": t0 + 3, "c1": "ddddd", "c2": 4_294_967_295},
    ]

    objname = "pandas_test_timeseries"

    with tables.open_file(temp_h5_path, mode="w") as f:
        t = f.create_table("/", name=objname, description=table_schema)
        for sample in testsamples:
            for key, value in sample.items():
                t.row[key] = value
            t.row.append()

    return temp_h5_path, objname, pd.DataFrame(testsamples)

