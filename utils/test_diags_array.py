
def test_diags_array():
    """Tests of diags_array that do not rely on diags wrapper."""
    diag = np.arange(1.0, 5.0)

    assert_array_equal(construct.diags_array(diag, dtype=None).toarray(), np.diag(diag))

    assert_array_equal(
        construct.diags_array(diag, offsets=2, dtype=None).toarray(), np.diag(diag, k=2)
    )

    assert_array_equal(
        construct.diags_array(diag, offsets=2, shape=(4, 4), dtype=None).toarray(),
        np.diag(diag, k=2)[:4, :4]
    )

    # Offset outside bounds when shape specified
    with pytest.raises(ValueError, match=".*out of bounds"):
        construct.diags(np.arange(1.0, 5.0), 5, shape=(4, 4))

