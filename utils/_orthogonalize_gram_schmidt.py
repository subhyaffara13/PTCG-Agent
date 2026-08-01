
def _orthogonalize_gram_schmidt(matrices, epsilon=0):
    """
    Apply Gram-Schmidt procedure to orthogonalize a batch of matrices.

    If epsilon is 0, this is equivalent to `torch.qr(matrices, out=(matrices, _))`,
    """
    num_cols = matrices.shape[2]
    for i in range(num_cols):
        # Normalize the i'th column.
        col = matrices[:, :, i : i + 1]
        # If no epsilon is added here, division by zero may be caused by vanishing gradients.
        # This epsilon is not needed if the input batch of matrices covers the gradients of at least one entire layer
        # in the neural network.
        if epsilon == 0:
            # Note that col ** 2 can underflow/overflow if we use FP16.
            # May need to consider multiplying a scaling factor and dividing it later, or using bfloat16 instead.
            try:
                col /= torch.norm(col, dim=1, keepdim=True)
            except ZeroDivisionError:
                logger.error(
                    "The matrices to be orthogonalized has at least a column of all 0s. Please set a small value such as 1e-8 "
                    "as `orthogonalization_epsilon` in PowerSGD state."
                )
                # Recover the values from NaNs to 0s.
                col.fill_(0.0)
        else:
            col /= torch.norm(col, dim=1, keepdim=True) + epsilon
        # Project it on the rest and remove it.
        if i + 1 < num_cols:
            rest = matrices[:, :, i + 1 :]
            rest -= torch.sum(col * rest, dim=1, keepdim=True) * col

