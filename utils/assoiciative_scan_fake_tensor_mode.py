
def assoiciative_scan_fake_tensor_mode(mode, combine_fn, xs, additional_inputs):
    with mode:
        return tuple(x.clone() for x in xs)

