
def _real_and_imag_input(fn, complex_inp_indices, tupled_inputs):
    # returns new functions that take real inputs instead of complex inputs as
    # (x, y) -> fn(x + y * 1j). And it computes: inp -> fn(inp + y * 1j) and inp -> fn(x + inp * 1j).
    # In each case, the other part is considered constant.
    # We do not use 0 for the constant here to make sure we always call the user function with a valid input.
    def apply_to_c_inps(fn, fn_to_apply):
        def wrapped_fn(*inputs):
            new_inputs = list(inputs)
            for should_be_complex in complex_inp_indices:
                new_inputs[should_be_complex] = fn_to_apply(
                    new_inputs[should_be_complex], tupled_inputs[should_be_complex]
                )
            return _as_tuple(fn(*new_inputs))

        return wrapped_fn

    real_fn = apply_to_c_inps(fn, lambda inp, orig: inp + orig.imag * 1j)
    imag_fn = apply_to_c_inps(fn, lambda inp, orig: orig.real + inp * 1j)
    return real_fn, imag_fn

