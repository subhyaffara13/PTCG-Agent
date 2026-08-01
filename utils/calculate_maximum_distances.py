
def calculate_maximum_distances(Z, xp):
    # Used for testing correctness of maxdists.
    n = Z.shape[0] + 1
    B = xp.zeros((n-1,), dtype=Z.dtype)
    for i in range(0, n - 1):
        q = xp.zeros((3,))
        left = Z[i, 0]
        right = Z[i, 1]
        if left >= n:
            b_left = B[xp.asarray(left, dtype=xp.int64) - n]
            q = xpx.at(q, 0).set(b_left)
        if right >= n:
            b_right = B[xp.asarray(right, dtype=xp.int64) - n]
            q = xpx.at(q, 1).set(b_right)
        q = xpx.at(q, 2).set(Z[i, 2])
        B = xpx.at(B, i).set(xp.max(q))
    return B

