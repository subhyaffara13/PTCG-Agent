import os

def test_multiple_open():
    # Ticket #1039, on Windows: check that files are not left open
    tmpdir = mkdtemp()
    try:
        x = dict(x=np.zeros((2, 2)))

        fname = pjoin(tmpdir, "a.mat")

        # Check that file is not left open
        savemat(fname, x)
        os.unlink(fname)
        savemat(fname, x)
        loadmat(fname)
        os.unlink(fname)

        # Check that stream is left open
        f = open(fname, 'wb')
        savemat(f, x)
        f.seek(0)
        f.close()

        f = open(fname, 'rb')
        loadmat(f)
        f.seek(0)
        f.close()
    finally:
        shutil.rmtree(tmpdir)

