
def test_compare_complex_dtypes():
    # GH 28050
    df = pd.DataFrame(np.arange(5).astype(np.complex128))
    msg = "'<' not supported between instances of 'complex' and 'complex'"

    with pytest.raises(TypeError, match=msg):
        df < df.astype(object)

    with pytest.raises(TypeError, match=msg):
        df.lt(df.astype(object))

