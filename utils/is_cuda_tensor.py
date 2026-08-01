
def is_cuda_tensor(obj):
    return (
        isinstance(obj, torch.Tensor) and
        obj.device.type == "cuda" and
        not isinstance(obj, torch._subclasses.FakeTensor)
    )

