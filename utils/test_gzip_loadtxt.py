
def test_gzip_loadtxt():
    # Thanks to another windows brokenness, we can't use
    # NamedTemporaryFile: a file created from this function cannot be
    # reopened by another open call. So we first put the gzipped string
    # of the test reference array, write it to a securely opened file,
    # which is then read from by the loadtxt function
    s = BytesIO()
    g = gzip.GzipFile(fileobj=s, mode='w')
    g.write(b'1 2 3\n')
    g.close()

    s.seek(0)
    with temppath(suffix='.gz') as name:
        with open(name, 'wb') as f:
            f.write(s.read())
        res = np.loadtxt(name)
    s.close()

    assert_array_equal(res, [1, 2, 3])

