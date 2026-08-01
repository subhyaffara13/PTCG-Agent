
def _softmax_backward_data(
    grad_output: Tensor, output: Tensor, dim: int, input_dtype: torch.dtype
):
    new_grad_output = grad_output * output
    grad_input = new_grad_output - output * torch.sum(
        new_grad_output, dim=dim, keepdim=True
    )

    # CPU kernel doesn't respect input_dtype, but following check doesn't work for meta tensor
    # if grad_output.device == torch.device("cpu"):
    #     return grad_input.contiguous()

    return _cast_grad_to_input_dtype(grad_output, grad_input, input_dtype).contiguous()


def _softmax_backward_data(
    grad_output: torch.Tensor,
    output: torch.Tensor,
    dim: int,
    input_dtype: torch.dtype,
) -> torch.Tensor:
    new_grad_output = grad_output * output
    sum_new_grad = torch.sum(new_grad_output, dim=dim, keepdim=True)
    # grad_input = new_grad_output - output * sum_new_grad
    grad_input = inductor_prims.fma(-output, sum_new_grad, new_grad_output)

    # CPU kernel doesn't respect input_dtype, but following check doesn't work for meta tensor
    # if grad_output.device == torch.device("cpu"):
    #     return grad_input.contiguous()

    if grad_output.dtype != input_dtype:
        grad_input = grad_input.to(input_dtype)
    return grad_input.contiguous()


def _softmax_backward_data(func, *args, **kwargs):
    _check_args_kwargs_length(args, kwargs, f"__torch_dispatch__, {func}", len_args=4)
    grad, output, dim, _input_dtype = args
    if is_masked_tensor(grad) and is_masked_tensor(output):
        if not _masks_match(grad, output):
            raise ValueError(
                f"__torch_dispatch__, {func}: expected the masks of grad and output to match"
            )
        grad_data = _get_data(grad)
        new_grad_data = torch.ops.aten._masked_softmax_backward(
            grad_data,
            _get_data(output),
            ~_maybe_get_mask(grad),
            dim % grad_data.ndim,
        )
        res = MaskedTensor(new_grad_data, _maybe_get_mask(grad))
        return res
    else:
        raise ValueError(
            f"__torch_dispatch__, {func}: grad and output must both be MaskedTensors"
        )

