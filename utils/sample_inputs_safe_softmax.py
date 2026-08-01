
def sample_inputs_safe_softmax(opinfo, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=False)

    def make_bool_mask(*shape):
        return torch.randint(0, 2, shape, device=device, dtype=torch.bool)

    def mask_two_rows(rows, cols):
        mask_two_rows = torch.ones((rows, cols), dtype=torch.bool, device=device)
        mask_two_rows[rows - 1] = False
        mask_two_rows[rows - 3] = False
        return mask_two_rows

    def convert_to_float_mask(mask: torch.Tensor) -> torch.Tensor:
        return torch.where(~mask, float('-inf'), 0.0)

    def with_requires_grad(tensor):
        return tensor.requires_grad_(requires_grad)

    def generate_input_from_mask(mask_shape, dim):
        mask = make_bool_mask(*mask_shape)
        input_tensor = make_arg(mask_shape)
        masked_input = input_tensor + convert_to_float_mask(mask)
        return SampleInput(with_requires_grad(masked_input), kwargs={'dim': dim})

    samples = [
        # Basic 3D tensor with mask
        generate_input_from_mask((2, 3, 4), dim=1),
        # 2D tensor with mask, testing different dim
        generate_input_from_mask((5, 5), dim=0),
        # 4D tensor, testing with a different dim
        generate_input_from_mask((2, 3, 4, 5), dim=2),
        # Edge case: 1D tensor
        generate_input_from_mask((10,), dim=0),
        # Edge case: tensor with one dimension of size 1
        generate_input_from_mask((1, 5, 5), dim=1),
        # Testing with all elements masked
        SampleInput(
            with_requires_grad(
                make_arg((3, 3))
                + convert_to_float_mask(
                    torch.zeros((3, 3), dtype=torch.bool, device=device)
                )
            ),
            kwargs={"dim": 1},
        ),
        # Testing with no elements masked
        SampleInput(
            with_requires_grad(
                make_arg((3, 3))
                + convert_to_float_mask(
                    torch.ones((3, 3), dtype=torch.bool, device=device)
                )
            ),
            kwargs={"dim": 1},
        ),
        # Testing with two rows masked
        SampleInput(
            with_requires_grad(
                make_arg((6, 3)) + convert_to_float_mask(mask_two_rows(6, 3))
            ),
            kwargs={"dim": 1},
        ),
    ]
    yield from samples

