
def test_gzip_loadtxt_from_string():
    s = BytesIO()
    f = gzip.GzipFile(fileobj=s, mode="w")
    f.write(b'1 2 3\n')
    f.close()
    s.seek(0)

    f = gzip.GzipFile(fileobj=s, mode="r")
    assert_array_equal(np.loadtxt(f), [1, 2, 3])

