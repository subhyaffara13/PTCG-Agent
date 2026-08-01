
def test_empty_npz(tmpdir):
    # Test for gh-9989
    fname = os.path.join(tmpdir, "nothing.npz")
    np.savez(fname)
    with np.load(fname) as nps:
        pass

