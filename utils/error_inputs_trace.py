
def error_inputs_trace(op, device):
    yield ErrorInput(SampleInput(make_tensor((3, 4, 5), dtype=torch.float32, device=device)), error_regex="expected a matrix")

