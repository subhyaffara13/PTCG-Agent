
def compute_error(y, y_true, rtol, atol):
    e = (y - y_true) / (atol + rtol * np.abs(y_true))
    return np.linalg.norm(e, axis=0) / np.sqrt(e.shape[0])

