
def _compare_owner_value(context_id, rref, grad):
    grads = dist_autograd.get_gradients(context_id)
    x = grads[rref.local_value()]
    if x.is_sparse:
        if not grad.is_sparse:
            raise AssertionError("Expected grad to be sparse")
        x = x.to_dense()
        grad = grad.to_dense()
    else:
        if grad.is_sparse:
            raise AssertionError("Expected grad to not be sparse")
    return torch.equal(x, grad)

