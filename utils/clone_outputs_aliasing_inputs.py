
def clone_outputs_aliasing_inputs(args):
    input_storage = {
        StorageWeakRef(arg._typed_storage())
        for arg in args
        if isinstance(arg, torch.Tensor)
    }

    def maybe_clone(t):
        if (
            isinstance(t, torch.Tensor)
            and StorageWeakRef(t._typed_storage()) in input_storage
        ):
            return t.clone()
        return t

    return maybe_clone

