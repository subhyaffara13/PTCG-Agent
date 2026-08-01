
def _to_numpy_array(input: torch.Tensor | int | float | str | bool) -> np.ndarray:
    if isinstance(input, (int, float, str, bool)):
        return ir.tensor(input).numpy()

    from torch.onnx._internal.exporter import _core

    return _core.TorchTensor(input).numpy()

