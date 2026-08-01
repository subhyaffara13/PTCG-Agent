
def scan_fake_tensor_mode(mode, combine_fn, init, xs, additional_inputs):
    with mode:
        scan_length = xs[0].shape[0]
        carry, outputs = _extract_carry_and_out(
            combine_fn(
                *init,
                *[first_slice_copy(inp) for inp in xs],
                *additional_inputs,
            ),
            len(init),
        )
        out = (
            *carry,
            *(stack_y(t, scan_length) for t in outputs),
        )
        return out

