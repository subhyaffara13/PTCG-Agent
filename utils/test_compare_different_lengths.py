
def test_compare_different_lengths():
    msg = "Can only compare identically-labeled Series objects"
    ser1 = pd.Series([1, 2, 3])
    ser2 = pd.Series([1, 2, 3, 4])
    with pytest.raises(ValueError, match=msg):
        ser1.compare(ser2)

