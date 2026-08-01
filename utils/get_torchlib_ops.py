
def get_torchlib_ops() -> tuple[_registration.OnnxDecompMeta, ...]:
    # Trigger op registration
    from torch.onnx._internal.exporter._torchlib import ops

    del ops
    if len(_registry) == 0:
        raise AssertionError("_registry must not be empty")
    return tuple(_registry)

