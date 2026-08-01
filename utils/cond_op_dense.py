
def cond_op_dense(pred, true_fn, false_fn, operands):
    if not all(isinstance(o, (torch.Tensor, int)) for o in operands):
        raise AssertionError(
            f"Dense implementation operands must be a list of tensors and ints {operands}"
        )
    mode = _get_current_dispatch_mode()
    if mode is not None:
        raise AssertionError("Mode should never be enabled for CPU/CUDA key")
    if pred:
        return true_fn(*operands)
    else:
        return false_fn(*operands)

