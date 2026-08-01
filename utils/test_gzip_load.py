
def test_gzip_load():
    a = np.random.random((5, 5))

    s = BytesIO()
    f = gzip.GzipFile(fileobj=s, mode="w")

    np.save(f, a)
    f.close()
    s.seek(0)

    f = gzip.GzipFile(fileobj=s, mode="r")
    assert_array_equal(np.load(f), a)

