
def strict_mode_op_dense(callable, operands):
    mode = _get_current_dispatch_mode()
    if mode is not None:
        raise AssertionError("Mode should never be enabled for CPU/CUDA key")
    return callable(*operands)

