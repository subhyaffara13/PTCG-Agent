
def temp_hdfstore(temp_h5_path):
    with HDFStore(temp_h5_path, mode="a") as store:
        yield store

