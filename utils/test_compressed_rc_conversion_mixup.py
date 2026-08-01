
def test_compressed_rc_conversion_mixup(op):
    # see gh-23826 for related discussion
    num_minor_axis = np.iinfo(np.uint32).max + 1
    minor_axis_index = np.array([num_minor_axis - 1])
    major_axis_index = np.array([10])
    row_cols = (minor_axis_index, major_axis_index)
    col_rows = (major_axis_index, minor_axis_index)

    X = csc_array((np.array([10]), row_cols), shape=(num_minor_axis, 20))
    X_2 = X.copy()
    # causes timeout error upon large memory alloc only if conversion to CSR occurs
    op(X_2, X)

    Z = csr_array((np.array([10]), col_rows), shape=(20, num_minor_axis))
    Z_2 = Z.copy()
    # causes timeout error upon large memory alloc only if conversion to CSC occurs
    op(Z_2, Z)

