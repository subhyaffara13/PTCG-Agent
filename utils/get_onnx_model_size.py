
def get_onnx_model_size(onnx_path: str, use_external_data_format: bool):
    if not use_external_data_format:
        return os.path.getsize(onnx_path)
    else:
        return sum([f.stat().st_size for f in Path(onnx_path).parent.rglob("*")])

