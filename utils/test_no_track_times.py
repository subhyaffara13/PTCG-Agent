import time

def test_no_track_times(temp_h5_path):
    # GH 32682
    # enables to set track_times (see `pytables` `create_table` documentation)

    def checksum(filename, hash_factory=hashlib.md5, chunk_num_blocks=128):
        h = hash_factory()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_num_blocks * h.block_size), b""):
                h.update(chunk)
        return h.digest()

    def create_h5_and_return_checksum(temp_h5_path, track_times):
        df = DataFrame({"a": [1]})

        with HDFStore(temp_h5_path, mode="w") as hdf:
            hdf.put(
                "table",
                df,
                format="table",
                data_columns=True,
                index=None,
                track_times=track_times,
            )

        return checksum(temp_h5_path)

    checksum_0_tt_false = create_h5_and_return_checksum(temp_h5_path, track_times=False)
    checksum_0_tt_true = create_h5_and_return_checksum(temp_h5_path, track_times=True)

    # sleep is necessary to create h5 with different creation time
    time.sleep(1)

    checksum_1_tt_false = create_h5_and_return_checksum(temp_h5_path, track_times=False)
    checksum_1_tt_true = create_h5_and_return_checksum(temp_h5_path, track_times=True)

    # checksums are the same if track_time = False
    assert checksum_0_tt_false == checksum_1_tt_false

    # checksums are NOT same if track_time = True
    assert checksum_0_tt_true != checksum_1_tt_true

