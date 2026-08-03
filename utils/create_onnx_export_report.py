import os

def create_onnx_export_report(
    filename: str | os.PathLike,
    formatted_traceback: str,
    program: torch.export.ExportedProgram,
    *,
    decomp_comparison: str | None = None,
    export_status: ExportStatus,
    profile_result: str | None,
    model: ir.Model | None = None,
    registry: _registration.ONNXRegistry | None = None,
    verification_result: str | None = None,
) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# PyTorch ONNX Conversion Report\n\n")
        f.write(_format_export_status(export_status))
        f.write("## Error messages\n\n")
        f.write("```pytb\n")
        f.write(formatted_traceback)
        f.write("\n```\n\n")
        f.write("## Exported program\n\n")
        f.write(_format_exported_program(program))
        if model is not None:
            f.write("## ONNX model\n\n")
            f.write("```python\n")
            f.write(str(model))
            f.write("\n```\n\n")
        f.write("## Analysis\n\n")
        _analysis.analyze(program, file=f, registry=registry)
        if decomp_comparison is not None:
            f.write("\n## Decomposition comparison\n\n")
            f.write(decomp_comparison)
            f.write("\n")
        if verification_result is not None:
            f.write("\n## Verification results\n\n")
            f.write(verification_result)
            f.write("\n")
        if profile_result is not None:
            f.write("\n## Profiling result\n\n")
            f.write("```\n")
            f.write(profile_result)
            f.write("```\n")

