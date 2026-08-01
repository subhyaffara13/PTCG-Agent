
def test_null_pointer():
    # Regression test for null pointers.
    s = readsav(path.join(DATA_PATH, 'null_pointer.sav'), verbose=False)
    assert_identical(s.point, None)
    assert_identical(s.check, np.int16(5))

