
def _combine_input_and_mask(op, input: MaskedTensor | Tensor, mask, *args) -> Tensor:
    def helper(input, mask):
        if mask is None:
            return input
        canonical_mask = _input_mask(input, mask=mask)
        if callable(op):
            fill_value = _reduction_identity(op.__name__, input, *args)
            return _where(canonical_mask, input, fill_value)
        else:
            raise ValueError(
                f"_combine_input_and_mask expected masked operation (got {type(op).__name__} object)"
            )

    class Combine(torch.autograd.Function):
        @staticmethod
        # pyrefly: ignore [bad-override]
        def forward(ctx, input, mask):
            """Return input with masked-out elements eliminated for the given operations."""
            ctx.save_for_backward(mask)

            if mask is not None:
                ctx.mark_non_differentiable(mask)

            return helper(input, mask)

        @staticmethod
        # pyrefly: ignore [bad-override]
        def backward(ctx, grad_output):
            (mask,) = ctx.saved_tensors
            grad_data = (
                grad_output.get_data() if is_masked_tensor(grad_output) else grad_output
            )
            result = as_masked_tensor(grad_data, mask)
            return result, None

    return (
        Combine.apply(input.get_data(), input.get_mask())  # type: ignore[union-attr]
        if is_masked_tensor(input)
        else helper(input, mask)
    )

