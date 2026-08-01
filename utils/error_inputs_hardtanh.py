
def error_inputs_hardtanh(op_info, device, **kwargs):
    # Tests that hardtanh errors out when passed min_val > max_val.
    yield ErrorInput(SampleInput(make_tensor((1,), dtype=torch.float, device=device), kwargs={"min_val": 0.5, "max_val": -0.5}),
                     error_type=ValueError, error_regex="min_val cannot be greater than max_val")

