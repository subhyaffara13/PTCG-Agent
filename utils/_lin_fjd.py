
def _lin_fjd(B, x):
    b = B[1:]
    b = np.repeat(b, (x.shape[-1],)*b.shape[-1], axis=0)
    return b.reshape(x.shape)

