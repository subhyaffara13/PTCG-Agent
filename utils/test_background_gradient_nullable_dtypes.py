
def test_background_gradient_nullable_dtypes():
    # GH 50712
    df1 = DataFrame([[1], [0], [np.nan]], dtype=float)
    df2 = DataFrame([[1], [0], [None]], dtype="Int64")

    ctx1 = df1.style.background_gradient()._compute().ctx
    ctx2 = df2.style.background_gradient()._compute().ctx
    assert ctx1 == ctx2

