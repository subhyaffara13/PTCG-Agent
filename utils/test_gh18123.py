
def test_gh18123(tmp_path):
    lines = [" %%MatrixMarket matrix coordinate real general\n",
             "5 5 3\n",
             "2 3 1.0\n",
             "3 4 2.0\n",
             "3 5 3.0\n"]
    test_file = tmp_path / "test.mtx"
    with open(test_file, "w") as f:
        f.writelines(lines)
    mmread(test_file, spmatrix=False)

