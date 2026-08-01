
def sample_inputs_to(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    # test_multiple_devices_to_cuda would fail if we use a different device than given
    devices = [device]
    if torch.device(device).type == 'cpu':
        devices = [torch.device('cpu'), torch.device('cuda:0')] if torch.cuda.is_available() else devices
    memory_formats = [torch.preserve_format, torch.channels_last]

    # TODO: can't switch `to.device` overload to use positional arguments
    # https://github.com/pytorch/pytorch/issues/84265
    # to.device overload
    for device, nb, cp, mem_f in product(devices, [True, False], [True, False], memory_formats):
        kwargs = {
            "memory_format": mem_f,
        }
        yield SampleInput(make_arg((S, S, S, S)), args=(device, torch.float64, nb, cp), kwargs=kwargs)

    other_dtype = torch.bfloat16 if torch.device(device).type == 'mps' else torch.float64

    # to.dtype overload
    for nb, cp, mem_f in product([True, False], [True, False], memory_formats):
        kwargs = {
            "memory_format": mem_f,
        }
        yield SampleInput(make_arg((S, S, S, S)), args=(other_dtype, nb, cp), kwargs=kwargs)

    # to.other overload
    for device, nb, cp, mem_f in product(devices, [True, False], [True, False], memory_formats):
        kwargs = {
            "memory_format": mem_f,
        }
        other = make_arg((S, S, S, S), dtype=other_dtype, device=device)
        yield SampleInput(make_arg((S, S, S, S)), args=(other, nb, cp), kwargs=kwargs)


def sample_inputs_to(op_info, device, dtype, requires_grad, op_kwargs=None, **kwargs):
    for njt in _sample_njts(
        device=device,
        dtype=dtype,
        requires_grad=requires_grad,
        dims=[2, 3, 4],
    ):
        other_dtypes = (
            d for d in (torch.float32, torch.half, torch.double) if d is not dtype
        )
        for other_dtype in other_dtypes:
            sample_name = f"{njt.dim()}D: {dtype} -> {other_dtype}"
            yield SampleInput(_clone(njt), kwargs={"dtype": dtype}, name=sample_name)

        # only include device transfer for CUDA inputs
        if "cuda" in device:
            other_device = "cpu"
            sample_name = f"{_describe_njt(njt)}: {device} -> {other_device}"
            yield SampleInput(
                _clone(njt), kwargs={"device": other_device}, name=sample_name
            )

