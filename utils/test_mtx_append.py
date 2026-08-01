
def test_mtx_append(tmp_path):
    a = mmread(io.StringIO("%%MatrixMarket matrix coordinate complex symmetric\n"
                           " 1 1 1\n"
                           "1 1 -2.1846000000000e+02  0.0000000000000e+00"),
               spmatrix=False)
    test_writefile = tmp_path / "test_mtx"
    test_readfile  = tmp_path / "test_mtx.mtx"
    mmwrite(test_writefile, a)
    mmread(test_readfile, spmatrix=False)

