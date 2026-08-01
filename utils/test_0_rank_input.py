
def test_0_rank_input():
    with pytest.raises(IndexError, match='tuple index out of range'):
        czt(5)
    with pytest.raises(IndexError, match='tuple index out of range'):
        zoom_fft(5, 0.5)

