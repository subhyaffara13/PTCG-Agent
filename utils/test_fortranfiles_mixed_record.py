
def test_fortranfiles_mixed_record(io_lock):
    filename = path.join(DATA_PATH, "fortran-mixed.dat")
    with io_lock:
        with FortranFile(filename, 'r', '<u4') as f:
            record = f.read_record('<i4,<f4,<i8,2<f8')

    assert_equal(record['f0'][0], 1)
    assert_allclose(record['f1'][0], 2.3)
    assert_equal(record['f2'][0], 4)
    assert_allclose(record['f3'][0], [5.6, 7.8])

