
def exported_program_to_ir(
    exported_program: torch.export.ExportedProgram,
    *,
    registry: _registration.ONNXRegistry | None = None,
    lower: Literal["at_conversion", "none"] = "at_conversion",
) -> ir.Model:
    """Convert an exported program to an ONNX IR model.

    Reference:
        - ExportedProgram spec: https://pytorch.org/docs/stable/export.ir_spec.html

    Args:
        exported_program: The exported program to convert.
        lower: Whether to lower the graph to core ONNX operators.
            at_conversion: Lower when translating the FX graph to ONNX IR.
            none: Do not lower the graph.
        registry: The registry of all ONNX Script decomposition.
    """
    if registry is None:
        registry = _registration.ONNXRegistry.from_torchlib()
    if lower != "none":
        exported_program = _prepare_exported_program_for_export(
            exported_program, registry=registry
        )
    return _exported_program_to_onnx_program(
        exported_program, registry=registry, lower=lower
    ).model

