
def kernel_matrix(x, kernel_func, xp):
    """Evaluate RBFs, with centers at `x`, at `x`."""
    return kernel_func(
        xp.linalg.vector_norm(x[None, :, :] - x[:, None, :], axis=-1), xp
    )

