
def test_large_file_support(tmpdir):
    if (sys.platform == 'win32' or sys.platform == 'cygwin'):
        pytest.skip("Unknown if Windows has sparse filesystems")
    # try creating a large sparse file
    tf_name = os.path.join(tmpdir, 'sparse_file')
    try:
        # seek past end would work too, but linux truncate somewhat
        # increases the chances that we have a sparse filesystem and can
        # avoid actually writing 5GB
        import subprocess as sp
        sp.check_call(["truncate", "-s", "5368709120", tf_name])
    except Exception:
        pytest.skip("Could not create 5GB large file")
    # write a small array to the end
    with open(tf_name, "wb") as f:
        f.seek(5368709120)
        d = np.arange(5)
        np.save(f, d)
    # read it back
    with open(tf_name, "rb") as f:
        f.seek(5368709120)
        r = np.load(f)
    assert_array_equal(r, d)

