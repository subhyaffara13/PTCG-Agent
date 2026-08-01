
def _allocate_jacobians_with_outputs(
    output_tensors: tuple, numel_input, dtype=None, device=None
) -> tuple[torch.Tensor, ...]:
    # Makes zero-filled tensors from outputs. If `dim` is not None, for each tensor
    # in `output_tensors`, returns a new zero-filled tensor with height of `dim` and
    # width of `t.numel`. Otherwise, for each tensor, returns a 1-d tensor with size
    # (t.numel,).
    options = {"dtype": dtype, "device": device, "layout": torch.strided}
    out: list[torch.Tensor] = [
        t.new_zeros((numel_input, t.numel()), **options)
        for t in output_tensors
        if _is_float_or_complex_tensor(t)
    ]
    return tuple(out)

