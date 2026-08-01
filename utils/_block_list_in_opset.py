
def _block_list_in_opset(name: str):
    def symbolic_fn(*args, **kwargs):
        raise errors.OnnxExporterError(
            f"ONNX export failed on {name}, which is not implemented for opset "
            f"{GLOBALS.export_onnx_opset_version}. "
            "Try exporting with other opset versions."
        )

    return symbolic_fn

