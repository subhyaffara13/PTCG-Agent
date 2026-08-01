
def is_in_onnx_export() -> bool:
    """Returns whether it is in the middle of ONNX export."""
    from torch.onnx._internal.exporter import _flags
    from torch.onnx._internal.torchscript_exporter._globals import GLOBALS

    return GLOBALS.in_onnx_export or _flags._is_onnx_exporting

