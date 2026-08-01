
def sample_inputs_erfcx(op_info, device, dtype, requires_grad, **kwargs):
    for shape in ((L,), (1, 0, 3), ()):
        yield SampleInput(
            make_tensor(
                shape,
                device=device,
                dtype=dtype,
                low=-5,
                requires_grad=requires_grad,
            ),
        )

