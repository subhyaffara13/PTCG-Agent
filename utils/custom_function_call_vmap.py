
def custom_function_call_vmap(
    interpreter: VmapInterpreter,
    autograd_function: type[torch.autograd.Function],
    *operands: Any,
    **kwargs: Any,
) -> Any:
    if any(
        isinstance(val, torch.Tensor)
        for val in torch.utils._pytree.tree_flatten(kwargs)[0]
    ):
        raise NotImplementedError(
            f"Run vmap on autograd.Function with kwarg-only Tensor args. "
            f"Please do not pass kwarg-only Tensors to autograd.Function. "
            f"Got: {kwargs}"
        )

    if autograd_function.generate_vmap_rule:
        if has_overridden_vmap_rule(autograd_function):
            # TODO: Update link to stable once that's out
            # https://github.com/pytorch/pytorch/issues/92029
            raise RuntimeError(
                f"You tried to vmap over {autograd_function.__name__}, but "
                f"it has both generate_vmap_rule=True and an overridden vmap "
                f"staticmethod. Please set generate_vmap_rule=False or delete "
                f"the overridden vmap staticmethod to avoid ambiguity. "
                f"For more details, please see "
                f"https://pytorch.org/docs/main/notes/extending.func.html"
            )
        return custom_function_call_vmap_generate_rule(
            interpreter, autograd_function, *operands
        )

    if not has_overridden_vmap_rule(autograd_function):
        # TODO: Update link to stable once that's out
        # https://github.com/pytorch/pytorch/issues/92029
        raise RuntimeError(
            f"You tried to vmap over {autograd_function.__name__}, but "
            f"it does not have vmap support. Please override and implement the "
            f"vmap staticmethod or set generate_vmap_rule=True. "
            f"For more details, please see "
            f"https://pytorch.org/docs/main/notes/extending.func.html"
        )

    return custom_function_call_vmap_helper(
        interpreter, autograd_function.vmap, autograd_function, *operands, **kwargs
    )

