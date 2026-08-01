
def _apply_fn_on_data(func, *args, **kwargs):
    return MaskedTensor(func(_get_data(args[0])), _maybe_get_mask(args[0]))

