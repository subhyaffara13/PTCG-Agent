
def test_lexsort_distinct_allocators():
    n = 40
    # ties in the primary key so the secondary key matters
    prim = np.array([f"{'p' * 20}{i % 5:03d}" for i in range(n)], dtype="T")
    sec = np.array(
        [f"{'s' * 20}{(7 * i) % n:03d}" for i in range(n)], dtype="T"
    )
    assert prim.dtype is not sec.dtype
    expected = np.lexsort((sec.astype("U30"), prim.astype("U30")))
    assert_array_equal(np.lexsort((sec, prim)), expected)

