
def test_array_scalar_ufunc_dtypes(op, dt1, dt2):
    # Same as above, but don't worry about sampling weird values so that we
    # do not have to sample as much
    arr1 = np.array(2, dtype=dt1)
    arr2 = np.array(3, dtype=dt2)  # some power do weird things.

    check_ufunc_scalar_equivalence(op, arr1, arr2)

