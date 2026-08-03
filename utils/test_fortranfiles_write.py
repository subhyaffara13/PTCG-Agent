import re

def test_fortranfiles_write():
    for filename in iglob(path.join(DATA_PATH, "fortran-*-*x*x*.dat")):
        m = re.search(r'fortran-([^-]+)-(\d+)x(\d+)x(\d+).dat', filename, re.I)
        if not m:
            raise RuntimeError(f"Couldn't match {filename} filename to regex")
        dims = (int(m.group(2)), int(m.group(3)), int(m.group(4)))

        dtype = m.group(1).replace('s', '<')
        data = np.arange(np.prod(dims)).reshape(dims).astype(dtype)

        tmpdir = tempfile.mkdtemp()
        try:
            testFile = path.join(str(threading.get_native_id()),
                                 tmpdir,path.basename(filename))
            f = FortranFile(testFile, 'w','<u4')
            f.write_record(data.T)
            f.close()
            originalfile = open(filename, 'rb')
            newfile = open(testFile, 'rb')
            assert_equal(originalfile.read(), newfile.read(),
                         err_msg=filename)
            originalfile.close()
            newfile.close()
        finally:
            shutil.rmtree(tmpdir)

