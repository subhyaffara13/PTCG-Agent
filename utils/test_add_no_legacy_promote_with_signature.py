
def test_add_no_legacy_promote_with_signature():
    # Possibly misplaced, but useful to test with string DType.  We check that
    # if there is clearly no loop found, a stray `dtype=` doesn't break things
    # Regression test for the bad error in gh-26735
    # (If legacy promotion is gone, this can be deleted...)
    with pytest.raises(TypeError, match=".*did not contain a loop"):
        np.add("3", 6, dtype=StringDType)

