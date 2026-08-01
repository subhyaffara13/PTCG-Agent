
def sample_inputs_linear(self, device, dtype, requires_grad, **kwargs):
    features_options = [[3, 4], [8, 8]]
    batch_options: list[list[int]] = [
        [],  # no batch
        [0],
        [8],
        [2, 3],
    ]
    create_tensor = partial(make_tensor, device=device, dtype=dtype,
                            requires_grad=requires_grad, low=-2, high=2)

    for has_bias, (in_feat, out_feat), batch_shape in \
            itertools.product([True, False], features_options, batch_options):
        input_tensor = create_tensor(batch_shape + [in_feat])
        weight = create_tensor([out_feat, in_feat])
        if not has_bias:
            yield SampleInput(input_tensor, weight)
            continue

        bias = create_tensor([out_feat])
        yield SampleInput(input_tensor, weight, bias)

    # 5D tensor, used to crash on MPS, see https://github.com/pytorch/pytorch/issues/114942
    yield SampleInput(create_tensor(2, 1, 2, 1, 2), create_tensor(4, 2))
    yield SampleInput(create_tensor(2, 1, 2, 1, 2), create_tensor(4, 2), create_tensor(4))

