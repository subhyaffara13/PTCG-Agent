
def test_fortran_roundtrip(tmpdir, io_lock):
    filename = path.join(str(tmpdir), str(threading.get_native_id()),
                         'test.dat')
    os.makedirs(path.dirname(filename), exist_ok=True)

    rng = np.random.RandomState(1)

    # double precision
    m, n, k = 5, 3, 2
    a = rng.randn(m, n, k)
    with FortranFile(filename, 'w') as f:
        f.write_record(a.T)
    with io_lock:
        a2 = read_unformatted_double(m, n, k, filename)

    with FortranFile(filename, 'r') as f:
        a3 = f.read_record('(2,3,5)f8').T
    assert_equal(a2, a)
    assert_equal(a3, a)

    # integer
    m, n, k = 5, 3, 2
    a = rng.randn(m, n, k).astype(np.int32)
    with FortranFile(filename, 'w') as f:
        f.write_record(a.T)
    with io_lock:
        a2 = read_unformatted_int(m, n, k, filename)
    with FortranFile(filename, 'r') as f:
        a3 = f.read_record('(2,3,5)i4').T
    assert_equal(a2, a)
    assert_equal(a3, a)

    # mixed
    m, n, k = 5, 3, 2
    a = rng.randn(m, n)
    b = rng.randn(k).astype(np.intc)
    with FortranFile(filename, 'w') as f:
        f.write_record(a.T, b.T)
    with io_lock:
        a2, b2 = read_unformatted_mixed(m, n, k, filename)
    with FortranFile(filename, 'r') as f:
        a3, b3 = f.read_record('(3,5)f8', '2i4')
        a3 = a3.T
    assert_equal(a2, a)
    assert_equal(a3, a)
    assert_equal(b2, b)
    assert_equal(b3, b)

