
def test_round_trip_current(typ, expected, pickle_writer, writer, temp_file):
    path = temp_file
    # test writing with each pickler
    pickle_writer(expected, path)

    # test reading with each unpickler
    result = pd.read_pickle(path)
    compare_element(result, expected, typ)

    result = python_unpickler(path)
    compare_element(result, expected, typ)

    # and the same for file objects (GH 35679)
    with open(path, mode="wb") as handle:
        writer(expected, path)
        handle.seek(0)  # shouldn't close file handle
    with open(path, mode="rb") as handle:
        result = pd.read_pickle(handle)
        handle.seek(0)  # shouldn't close file handle
    compare_element(result, expected, typ)

