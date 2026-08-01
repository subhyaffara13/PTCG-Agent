
def partial_apply_nontensors(fn, args, kwargs):
    inputs = SplitInputs(args, kwargs)

    def new_fn(*tensors_):
        tensors = iter(tensors_)
        full_args = [args[i] if s == 's' else next(tensors) for i, s in enumerate(inputs.arg_types)]
        full_kwargs = {k: kwargs[k] if s == 's' else next(tensors) for k, s in inputs.kwarg_types.items()}
        return fn(*full_args, **full_kwargs)

    return new_fn, inputs

