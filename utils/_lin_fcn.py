
def _lin_fcn(B, x):
    a, b = B[0], B[1:]
    b = b.reshape((b.shape[0], 1))

    return a + (x*b).sum(axis=0)

