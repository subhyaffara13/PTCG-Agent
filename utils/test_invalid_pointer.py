
def test_invalid_pointer():
    # Regression test for invalid pointers (gh-4613).

    # In some files in the wild, pointers can sometimes refer to a heap
    # variable that does not exist. In that case, we now gracefully fail for
    # that variable and replace the variable with None and emit a warning.
    # Since it's difficult to artificially produce such files, the file used
    # here has been edited to force the pointer reference to be invalid.
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        s = readsav(path.join(DATA_PATH, 'invalid_pointer.sav'), verbose=False)
    assert_(len(w) == 1)
    assert_(str(w[0].message) == ("Variable referenced by pointer not found in "
                                  "heap: variable will be set to None"))
    assert_identical(s['a'], np.array([None, None]))

