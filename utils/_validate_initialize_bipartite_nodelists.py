
def _validate_initialize_bipartite_nodelists(A, row_order, column_order):
    n, m = A.shape
    # Validate nodelists if provided
    if row_order is not None:
        if len(row_order) != n:
            raise ValueError(
                "Length of row_order does not match number of rows in A ({n})"
            )
    else:
        row_order = []

    if column_order is not None:
        if len(column_order) != m:
            raise ValueError(
                "Length of column_order does not match number of columns in A ({m})"
            )
    else:
        column_order = []

    return row_order, column_order

