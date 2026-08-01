
def test_fortranfiles_read(io_lock):
    for filename in iglob(path.join(DATA_PATH, "fortran-*-*x*x*.dat")):
        m = re.search(r'fortran-([^-]+)-(\d+)x(\d+)x(\d+).dat', filename, re.I)
        if not m:
            raise RuntimeError(f"Couldn't match {filename} filename to regex")

        dims = (int(m.group(2)), int(m.group(3)), int(m.group(4)))

        dtype = m.group(1).replace('s', '<')

        with io_lock:
            f = FortranFile(filename, 'r', '<u4')
            data = f.read_record(dtype=dtype).reshape(dims, order='F')
            f.close()

        expected = np.arange(np.prod(dims)).reshape(dims).astype(dtype)
        assert_equal(data, expected)

