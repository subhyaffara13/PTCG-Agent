
def test_infer_row_shape():
    # GH 17437
    # if row shape is changing, infer it
    df = DataFrame(np.random.default_rng(2).random((10, 2)))
    result = df.apply(np.fft.fft, axis=0).shape
    assert result == (10, 2)

    result = df.apply(np.fft.rfft, axis=0).shape
    assert result == (6, 2)

