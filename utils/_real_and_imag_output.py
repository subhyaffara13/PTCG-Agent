
def _real_and_imag_output(fn):
    # returns new functions real(fn), and imag(fn) where real(fn) and imag(fn) behave the same as
    # the original fn, except torch.real or torch.imag are applied to the complex outputs
    def apply_to_c_outs(fn, fn_to_apply):
        def wrapped_fn(*inputs):
            outs = _as_tuple(fn(*inputs))
            return tuple(fn_to_apply(o) if o.is_complex() else o for o in outs)

        return wrapped_fn

    return apply_to_c_outs(fn, torch.real), apply_to_c_outs(fn, torch.imag)

