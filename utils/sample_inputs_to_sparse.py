
def sample_inputs_to_sparse(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    yield SampleInput(make_arg((S, S))).with_metadata(output_process_fn_grad=lambda x: x.to_dense())
    yield SampleInput(make_arg((S, S)), 1).with_metadata(output_process_fn_grad=lambda x: x.to_dense())

