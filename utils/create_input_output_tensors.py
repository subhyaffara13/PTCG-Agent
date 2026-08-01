
def create_input_output_tensors(inputs, outputs, device):
    input_tensors = {name: torch.from_numpy(array).to(device) for name, array in inputs.items()}
    output_tensors = {name: torch.from_numpy(array).to(device) for name, array in outputs.items()}
    return input_tensors, output_tensors

