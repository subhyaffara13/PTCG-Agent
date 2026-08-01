
def optimize_longformer(onnx_model_path: str, fp32_model_path: str, fp16_model_path=None):
    """Optimize longformer onnx model

    Args:
        onnx_model_path (str): path of original ONNX model.
        fp32_model_path (str): path of optimized fp32 model.
        fp16_model_path (str, optional): path of optimized fp16 model. Defaults to None.
    """
    model = load_model(onnx_model_path, format=None, load_external_data=True)
    optimizer = BertOnnxModel(model)
    optimizer.optimize()

    use_external_data_format = False
    if fp32_model_path:
        optimizer.save_model_to_file(fp32_model_path, use_external_data_format)
        print(f"optimized fp32 model saved to {fp32_model_path}")

    if fp16_model_path:
        optimizer.convert_float_to_float16(keep_io_types=True)
        optimizer.save_model_to_file(fp16_model_path, use_external_data_format)
        print(f"optimized fp16 model saved to {fp16_model_path}")

