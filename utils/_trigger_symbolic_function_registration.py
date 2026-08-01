
def _trigger_symbolic_function_registration() -> None:
    """Trigger the registration of symbolic functions for all supported opsets."""

    from torch.onnx._internal.torchscript_exporter import (  # noqa: F401
        symbolic_opset10,
        symbolic_opset11,
        symbolic_opset12,
        symbolic_opset13,
        symbolic_opset14,
        symbolic_opset15,
        symbolic_opset16,
        symbolic_opset17,
        symbolic_opset18,
        symbolic_opset19,
        symbolic_opset20,
        symbolic_opset7,
        symbolic_opset8,
        symbolic_opset9,
    )

