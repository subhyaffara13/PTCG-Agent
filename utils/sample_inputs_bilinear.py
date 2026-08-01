
def sample_inputs_bilinear(self, device, dtype, requires_grad, **kwargs):
    features_options = [[3, 4, 5], [8, 8, 8]]
    batch_options: list[list[int]] = [
        [],  # no batch
        [0],
        [8],
        [2, 3],
    ]
    create_tensor = partial(make_tensor, device=device, dtype=dtype,
                            requires_grad=requires_grad, low=-2, high=2)

    for has_bias, (in_feat1, in_feat2, out_feat), batch_shape in \
            itertools.product([True, False], features_options, batch_options):
        input_tensor1 = create_tensor(batch_shape + [in_feat1])
        input_tensor2 = create_tensor(batch_shape + [in_feat2])
        weight = create_tensor([out_feat, in_feat1, in_feat2])
        if not has_bias:
            yield SampleInput(input_tensor1, input_tensor2, weight)
            continue
        bias = create_tensor([out_feat])
        yield SampleInput(input_tensor1, input_tensor2, weight, bias)

