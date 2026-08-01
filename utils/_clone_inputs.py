
def _clone_inputs(args):
    def clone_input(a):
        if a is None:
            return None
        elif isinstance(a, torch.Tensor):
            # TODO: figure out one liner to .clone() and set requires_grad
            v = (
                a.detach()
                .clone(memory_format=None if a.is_mkldnn else torch.preserve_format)
                .requires_grad_(a.requires_grad)
            )
            if a.grad is not None:
                v.grad = clone_input(v.grad)
            return v
        else:
            return a.clone(memory_format=torch.preserve_format)

    # pyrefly: ignore [missing-attribute]
    return function._nested_map(
        lambda x: isinstance(x, torch.Tensor), clone_input, condition_msg="tensors"
    )(args)

