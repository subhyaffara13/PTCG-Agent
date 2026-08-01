
def CompileSpec(
    inputs,
    outputs,
    backend=CoreMLComputeUnit.CPU,
    allow_low_precision=True,
    quantization_mode=CoreMLQuantizationMode.NONE,
    mlmodel_export_path=None,
    convert_to=None,
):
    return (
        inputs,
        outputs,
        backend,
        allow_low_precision,
        quantization_mode,
        mlmodel_export_path,
        convert_to,
    )

