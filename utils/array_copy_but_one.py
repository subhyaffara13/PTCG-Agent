
def array_copy_but_one(a, r, c, v):
    z = np.array(a, copy=True)
    z[r, c] = v
    return z

