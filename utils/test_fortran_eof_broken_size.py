import os

def test_fortran_eof_broken_size(tmpdir):
    filename = path.join(str(tmpdir), str(threading.get_native_id()),
                         "scratch")
    os.makedirs(path.dirname(filename), exist_ok=True)
    rng = np.random.RandomState(1)
    with FortranFile(filename, 'w') as f:
        f.write_record(rng.randn(5))
        f.write_record(rng.randn(3))
    with open(filename, "ab") as f:
        f.write(b"\xff")
    with FortranFile(filename, 'r') as f:
        assert len(f.read_reals()) == 5
        assert len(f.read_reals()) == 3
        with pytest.raises(FortranFormattingError):
            f.read_reals()

