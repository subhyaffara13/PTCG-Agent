
def build_dynamic_axes(example_inputs, outputs_flatten):
    sequence_length = example_inputs["input_ids"].shape[-1]

    dynamic_axes = {key: {0: "batch_size", 1: "seq_len"} for key in example_inputs}

    output_names = ["output_" + str(i + 1) for i in range(len(outputs_flatten))]
    for i, output_name in enumerate(output_names):
        dynamic_axes[output_name] = {0: "batch_size"}
        dims = outputs_flatten[i].shape
        for j, dim in enumerate(dims):
            if dim == sequence_length:
                dynamic_axes[output_name].update({j: "seq_len"})
    return dynamic_axes, output_names

