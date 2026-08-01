
def reference_inputs_upsample(mode, self, device, dtype, requires_grad, **kwargs):
    yield from sample_inputs_upsample(mode, self, device, dtype, requires_grad, **kwargs)

    if mode == 'bilinear':
        make_arg = partial(
            make_tensor,
            device=device,
            dtype=dtype,
            requires_grad=requires_grad,
            # we pick more realistic upper bound 256 instead of default 10 for uint8 dtype
            high=256 if dtype == torch.uint8 else None,
        )
        # provide a single sample for more typical image processing usage
        for memory_format in [torch.contiguous_format, torch.channels_last]:
            yield SampleInput(
                make_arg((2, 3, 345, 456), memory_format=memory_format),
                (270, 270),
            )

