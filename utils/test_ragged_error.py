
def test_ragged_error():
    rows = ["1,2,3", "1,2,3", "4,3,2,1"]
    with pytest.raises(ValueError,
            match="the number of columns changed from 3 to 4 at row 3"):
        np.loadtxt(rows, delimiter=",")

