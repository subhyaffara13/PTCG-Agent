import os

def test_fspath(temp_h5_path):
    with HDFStore(temp_h5_path) as store:
        assert os.fspath(store) == str(temp_h5_path)


def test_fspath(fmt, tmp_path):
    out = tmp_path / f"test.{fmt}"
    plt.savefig(out)
    with out.open("rb") as file:
        # All the supported formats include the format name (case-insensitive)
        # in the first 100 bytes.
        assert fmt.encode("ascii") in file.read(100).lower()

