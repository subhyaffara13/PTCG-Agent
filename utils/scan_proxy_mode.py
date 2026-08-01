
def scan_proxy_mode(mode, combine_fn, init, xs, additional_inputs):
    return trace_scan(mode, scan_op, combine_fn, init, xs, additional_inputs)

