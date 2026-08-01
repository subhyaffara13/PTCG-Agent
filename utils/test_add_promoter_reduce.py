
def test_add_promoter_reduce():
    # Exact TypeError could change, but ensure StringDtype doesn't match
    with pytest.raises(TypeError, match="the resolved dtypes are not"):
        np.add.reduce(np.array(["a", "b"], dtype="U"))

    # On the other hand, using `dtype=T` in the *ufunc* should work.
    np.add.reduce(np.array(["a", "b"], dtype="U"), dtype=np.dtypes.StringDType)

