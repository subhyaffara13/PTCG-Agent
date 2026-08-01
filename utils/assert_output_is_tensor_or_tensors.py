
def assert_output_is_tensor_or_tensors(output: Any, api: str) -> None:
    if isinstance(output, torch.Tensor):
        return
    if not isinstance(output, tuple):
        raise RuntimeError(
            f"{api}: Expected output of f to be a Tensor or Tensors, got {type(output)}"
        )
    if len(output) == 0:
        raise RuntimeError(
            f"{api}: Expected output of f to be a non-empty tuple of Tensors."
        )
    for out in output:
        if isinstance(out, torch.Tensor):
            continue
        raise RuntimeError(
            f"{api}: Expected output of f to be a Tensor or Tensors, got "
            f"{type(out)} as an output"
        )

