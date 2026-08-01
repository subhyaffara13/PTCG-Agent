
def sample_inputs_where(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    def make_bool_mask(shape):
        # Make sure at least one element is nonzero,
        # except for empty tensor
        mask_t = make_tensor(shape, dtype=torch.bool, device=device, requires_grad=False)

        if mask_t.numel() == 0:
            return mask_t
        elif mask_t.numel() == 1:
            mask_t.fill_(True)
            return mask_t

        if mask_t.sum() == 0:
            def random_index(shape):
                return tuple(random.randrange(0, max_idx) for max_idx in shape)

            mask_t[random_index(mask_t.shape)] = True
            return mask_t

        return mask_t

    cases = (((M, M), (M, M), (M, M), False),
             ((M, 1, M), (M, M), (M, M, 1), True),
             ((), (), (), False),
             ((M, 1, M), (), (M, M, 1), True),
             ((), (M, M), (), True),
             ((), (2), (1, 1), True),
             )

    for shape, mask_shape, other_shape, broadcasts_input in cases:
        yield SampleInput(make_arg(shape),
                          args=(make_bool_mask(mask_shape), make_arg(other_shape)),
                          broadcasts_input=broadcasts_input)


def sample_inputs_where(op_info, device, dtype, requires_grad, **kwargs):
    for sample in sample_inputs_elementwise_njt_binary(
        op_info, device, dtype, requires_grad, **kwargs
    ):
        other = sample.args[0]
        sample.args = ()
        sample.kwargs["other"] = other
        sample.kwargs["condition"] = sample.input > 0.0
        sample.name = sample.name.replace("(", "(NT, ")
        yield sample

