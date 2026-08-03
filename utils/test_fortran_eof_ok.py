import os

def test_fortran_eof_ok(tmpdir):
    filename = path.join(str(tmpdir), str(threading.get_native_id()),
                         "scratch")
    os.makedirs(path.dirname(filename), exist_ok=True)
    rng = np.random.RandomState(1)
    with FortranFile(filename, 'w') as f:
        f.write_record(rng.randn(5))
        f.write_record(rng.randn(3))
    with FortranFile(filename, 'r') as f:
        assert len(f.read_reals()) == 5
        assert len(f.read_reals()) == 3
        with pytest.raises(FortranEOFError):
            f.read_reals()

