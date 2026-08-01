
def _unflatten_tensor(tensor, spec, *, device_handle=None, compute_stream=None):
    # unflatten would mainly be called every time FSDP allgather parameters.
    result = DTensor.from_local(
        tensor,
        spec.mesh,
        spec.placements,
        run_check=False,
        shape=spec.shape,
        stride=spec.stride,
    )
    if tensor.requires_grad:
        # only register the hook if the tensor requires grad
        tensor.register_hook(
            partial(
                sync_grad_hook,
                device_handle=device_handle,
                compute_stream=compute_stream,
            )
        )
    return result

