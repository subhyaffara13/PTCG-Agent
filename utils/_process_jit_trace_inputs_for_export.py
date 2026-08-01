
def _process_jit_trace_inputs_for_export(example_inputs, example_kwarg_inputs):
    if not isinstance(example_inputs, (tuple, list, dict)):
        example_inputs = (example_inputs,)

    elif isinstance(example_inputs, list):
        example_inputs = tuple(example_inputs)

    elif (
        isinstance(example_inputs, (torch.Tensor, dict))
        and example_kwarg_inputs is None
    ):
        example_inputs = (example_inputs,)

    if example_kwarg_inputs is None:
        example_kwarg_inputs = {}
    return example_inputs, example_kwarg_inputs

