
def generate_subclass_choices_args_kwargs(args, kwargs, CCT, cct_mode):
    # CCT: CompositeCompliantTensor class which is generated using generate_cct_and_mode
    flat_kwargs, spec = tree_flatten(kwargs)
    flat_args_kwargs = list(args) + list(flat_kwargs)
    for choice, debug_metadata in generate_subclass_choices(flat_args_kwargs, CCT, cct_mode):
        new_args = choice[:len(args)]
        new_kwargs = tree_unflatten(choice[len(args):], spec)
        which_args_are_wrapped = debug_metadata[:len(args)]
        which_kwargs_are_wrapped = tree_unflatten(debug_metadata[len(args):], spec)
        yield new_args, new_kwargs, which_args_are_wrapped, which_kwargs_are_wrapped

