
def modify_mesh(x, insert_1, insert_2):
    """Insert nodes into a mesh.

    Nodes removal logic is not established, its impact on the solver is
    presumably negligible. So, only insertion is done in this function.

    Parameters
    ----------
    x : ndarray, shape (m,)
        Mesh nodes.
    insert_1 : ndarray
        Intervals to each insert 1 new node in the middle.
    insert_2 : ndarray
        Intervals to each insert 2 new nodes, such that divide an interval
        into 3 equal parts.

    Returns
    -------
    x_new : ndarray
        New mesh nodes.

    Notes
    -----
    `insert_1` and `insert_2` should not have common values.
    """
    # Because np.insert implementation apparently varies with a version of
    # NumPy, we use a simple and reliable approach with sorting.
    return np.sort(np.hstack((
        x,
        0.5 * (x[insert_1] + x[insert_1 + 1]),
        (2 * x[insert_2] + x[insert_2 + 1]) / 3,
        (x[insert_2] + 2 * x[insert_2 + 1]) / 3
    )))

