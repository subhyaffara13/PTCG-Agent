
def generate_subclass_choices(flat_args, CCT, cct_mode):
    # CCT: CompositeCompliantTensor class which is generated using generate_cct_and_mode
    is_tensor_likes = [isinstance(arg, torch.Tensor) or is_tensorlist(arg) for arg in flat_args]
    subclass_options = [[False, True] if is_tensor_like else [False] for is_tensor_like in is_tensor_likes]

    for which_args_are_wrapped in itertools.product(*subclass_options):

        result = [maybe_map(partial(wrap, CCT=CCT, cct_mode=cct_mode), should_wrap_arg, arg)
                  for should_wrap_arg, arg in zip(which_args_are_wrapped, flat_args, strict=True)]
        yield result, which_args_are_wrapped

