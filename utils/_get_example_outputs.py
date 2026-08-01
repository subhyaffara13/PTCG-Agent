
def _get_example_outputs(model, args):
    input_args = copy.deepcopy(args)
    input_kwargs = {}
    if input_args and isinstance(input_args[-1], dict):
        input_kwargs = input_args[-1]
        input_args = input_args[:-1]

    example_outputs = model(*input_args, **input_kwargs)
    if isinstance(example_outputs, list):
        example_outputs = [example_outputs]
    elif not isinstance(example_outputs, tuple):
        example_outputs = (example_outputs,)

    return example_outputs

