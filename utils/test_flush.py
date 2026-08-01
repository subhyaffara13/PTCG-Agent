
def test_flush(capfd):
    msg = "(not flushed)"
    msg2 = "(flushed)"

    with m.ostream_redirect():
        m.noisy_function(msg, flush=False)
        stdout, stderr = capfd.readouterr()
        assert not stdout

        m.noisy_function(msg2, flush=True)
        stdout, stderr = capfd.readouterr()
        assert stdout == msg + msg2

        m.noisy_function(msg, flush=False)

    stdout, stderr = capfd.readouterr()
    assert stdout == msg


def test_flush(temp_h5_path):
    with HDFStore(temp_h5_path, mode="w") as store:
        store["a"] = Series(range(5))
        store.flush()
        store.flush(fsync=True)

