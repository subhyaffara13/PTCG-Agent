
def error_inputs_embedding(op_info, device, **kwargs):
    indices = torch.rand(2, 2, device=device).long()
    weights = [
        torch.tensor(1.0, device=device),
        torch.tensor(1.0, device=device).reshape(1, 1, 1),
    ]

    for weight in weights:
        yield ErrorInput(SampleInput(weight, args=(indices,)), error_type=RuntimeError,
                         error_regex="'weight' must be 2-D")

