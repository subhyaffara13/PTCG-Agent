
def associative_scan_op_dense(combine_fn, xs, additional_inputs):
    return generic_associative_scan(combine_fn, xs, additional_inputs=additional_inputs)

