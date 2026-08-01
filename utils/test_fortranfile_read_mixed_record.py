
def test_fortranfile_read_mixed_record(io_lock):
    # The data file fortran-3x3d-2i.dat contains the program that
    # produced it at the end.
    #
    # double precision :: a(3,3)
    # integer :: b(2)
    # ...
    # open(1, file='fortran-3x3d-2i.dat', form='unformatted')
    # write(1) a, b
    # close(1)
    #

    filename = path.join(DATA_PATH, "fortran-3x3d-2i.dat")
    with io_lock:
        with FortranFile(filename, 'r', '<u4') as f:
            record = f.read_record('(3,3)<f8', '2<i4')

    ax = np.arange(3*3).reshape(3, 3).astype(np.float64)
    bx = np.array([-1, -2], dtype=np.int32)

    assert_equal(record[0], ax.T)
    assert_equal(record[1], bx.T)

