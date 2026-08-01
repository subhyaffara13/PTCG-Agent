
def sample_inputs_clone(op_info, device, dtype, requires_grad, **kwargs):
    # non-contiguous NJTs
    for njt in _sample_njts(
        device=device, dtype=dtype, requires_grad=requires_grad, dims=[2, 3, 4]
    ):
        yield SampleInput(njt, name=_describe_njt(njt))

    for memory_format in (torch.contiguous_format, torch.preserve_format):
        # construct a "non-contiguous with holes" NJT
        values = torch.randn(
            10, 5, device=device, dtype=dtype, requires_grad=requires_grad
        )
        offsets = torch.tensor([0, 2, 4, 10], device=device, dtype=torch.int64)
        lengths = torch.tensor([2, 1, 3], device=device, dtype=torch.int64)
        njt = torch.nested.nested_tensor_from_jagged(
            values, offsets=offsets, lengths=lengths
        )

        njt_desc = _describe_njt(njt)
        yield SampleInput(
            njt,
            kwargs={"memory_format": memory_format},
            name=f"{njt_desc}: {memory_format})",
        )

