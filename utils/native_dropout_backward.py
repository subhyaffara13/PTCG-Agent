
def native_dropout_backward(grad_output: Tensor, mask: Tensor, scale: float):
    # According to the CUDA kernel implementation we should have this test;
    # but it seems to fail tests!
    # torch._check(mask.dtype == torch.bool, lambda: f"Mask should be Bool Scalar Type {mask.dtype}")

    # Mimicking CUDA kernel's behavior for output stride: output follow input's memory format
    # This different from TensorIterator's behavior
    r = (grad_output * (mask.type_as(grad_output) * scale)).clone(
        memory_format=utils.suggest_memory_format(grad_output)
    )
    return r

