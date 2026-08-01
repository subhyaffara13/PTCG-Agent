
def reference_hardsigmoid(x):
    intermediate = x / 6 + 0.5
    y = np.clip(intermediate, 0, None)
    return np.where(y > 1, 1, y).astype(x.dtype)

