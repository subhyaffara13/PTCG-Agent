
def error_inputs_kthvalue(op_info, device, **kwargs):
    # tests overlapping output fails
    t = make_tensor(10, dtype=torch.float32, device=device)
    indices = torch.empty((), device=device, dtype=torch.long)
    yield ErrorInput(SampleInput(t, 5, out=(t, indices)),
                     error_regex="unsupported operation")

    k_out_of_range_err = "selected number k out of range for dimension"
    yield ErrorInput(SampleInput(torch.randn(2, 2, device=device), 3, 0),
                     error_regex=k_out_of_range_err)
    yield ErrorInput(SampleInput(torch.randn(2, 2, device=device), 3),
                     error_regex=k_out_of_range_err)
    yield ErrorInput(SampleInput(torch.tensor(2, device=device), 3),
                     error_regex=k_out_of_range_err)

