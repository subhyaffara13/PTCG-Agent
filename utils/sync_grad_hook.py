
def sync_grad_hook(grad, *, device_handle=None, compute_stream=None):
    if isinstance(grad, AsyncCollectiveTensor):
        if compute_stream is not None:
            with device_handle.stream(compute_stream):
                grad = grad.wait()
        else:
            grad = grad.wait()

    return grad

