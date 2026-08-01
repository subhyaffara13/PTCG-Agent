
def test_gh11389():
    mmread(io.StringIO("%%MatrixMarket matrix coordinate complex symmetric\n"
                       " 1 1 1\n"
                       "1 1 -2.1846000000000e+02  0.0000000000000e+00"),
           spmatrix=False)

