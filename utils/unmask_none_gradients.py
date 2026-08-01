
def unmask_none_gradients(grads, operands):
    allowed_types = (torch.Tensor, int, torch.SymInt)
    if not all(isinstance(o, allowed_types) for o in operands):
        raise AssertionError(
            f"operands can only be of {allowed_types} but got {[type(o) for o in operands]}"
        )

    unmasked_grads = []
    for g, o in zip(grads, operands):
        if g is not None:
            unmasked_grads.append(g)
        else:
            # In case the operand is an int or a torch.SymInt, return None
            # This can happen for lifted_arguments. E.g., the shapes of a dynamic tensor are lifted and passed
            # as additional arguments
            unmasked_grads.append(
                torch.zeros_like(o) if isinstance(o, torch.Tensor) else None
            )

    return unmasked_grads

