
def scan_op_dense(combine_fn, init, xs, additional_inputs):
    mode = _get_current_dispatch_mode()
    if mode is not None:
        raise AssertionError("Mode should never be enabled for CPU/CUDA key")
    return generic_scan(combine_fn, init, xs, additional_inputs=additional_inputs)

