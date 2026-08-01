
def check_itemsize(n_elem, dt):
    if dt == "T":
        return np.dtype(dt).itemsize
    if dt == "S":
        return n_elem
    if dt == "U":
        return n_elem * 4

