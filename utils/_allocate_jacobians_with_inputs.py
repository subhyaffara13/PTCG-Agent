
def _allocate_jacobians_with_inputs(
    input_tensors: tuple, numel_output
) -> tuple[torch.Tensor, ...]:
    # Makes zero-filled tensors from inputs. If `numel_output` is not None, for
    # each tensor in `input_tensors`, returns a new zero-filled tensor with height
    # of `t.numel` and width of `numel_output`. Otherwise, for each tensor, returns
    # a 1-d tensor with size `(t.numel,)`. Each new tensor will be strided and have
    # the same dtype and device as those of the corresponding input.
    out: list[torch.Tensor] = [
        t.new_zeros((t.numel(), numel_output), layout=torch.strided)
        for t in input_tensors
        if _is_float_or_complex_tensor(t) and t.requires_grad
    ]
    return tuple(out)

