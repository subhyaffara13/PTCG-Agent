
def _get_batch_norm_reserve_tensor(
    input: Tensor,
    weight: Tensor | None,
    bias: Tensor | None,
    running_mean: Tensor,
    running_var: Tensor,
    eps: float,
    training: bool,
) -> Tensor:
    """
    Return a reserve tensor for batch norm, used only by cudnn to pass forward state to the
    backward pass. This is needed for `_batch_norm_with_update` and `_batch_norm_no_update`,
    which support a variety of backends including cudnn. We create this tensor here to get
    the correct shape in the traced graph if we detect that will call the cudnn kernel,
    and rely on DCE to avoid materializing this tensor.
    """
    backend = torch._C._select_batch_norm_backend(  # type: ignore[attr-defined]
        input, weight, bias, running_mean, running_var, True, eps
    )
    reserve_size = 0
    if backend == torch._C._BatchNormBackend.Cudnn:  # type: ignore[attr-defined]
        reserve_size = torch._C._get_cudnn_batch_norm_reserve_space_size(  # type: ignore[attr-defined]
            input, training
        )
    return torch.empty(
        reserve_size, dtype=torch.uint8, layout=input.layout, device=input.device
    )

