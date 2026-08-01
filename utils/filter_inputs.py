
def filter_inputs(inputs, input_names):
    remaining_model_inputs = {}
    for input_name in input_names:
        if input_name in inputs:
            remaining_model_inputs[input_name] = inputs[input_name]
    return remaining_model_inputs

