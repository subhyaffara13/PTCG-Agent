
def test_pickle_reader(reader):
    # GH 22265
    with BytesIO() as buffer:
        pickle.dump(reader, buffer)

