
def test_malicious_load():
    class Executor:
        def __reduce__(self):
            return (assert_, (False, 'unexpected code execution'))

    fd, tmpfile = tempfile.mkstemp(suffix='.npz')
    os.close(fd)
    try:
        np.savez(tmpfile, format=Executor())

        # Should raise a ValueError, not execute code
        assert_raises(ValueError, load_npz, tmpfile)
    finally:
        os.remove(tmpfile)

