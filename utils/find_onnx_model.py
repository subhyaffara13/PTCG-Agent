import os

def find_onnx_model(model_name, onnx_dir="."):
    # Search onnx model in the following order: optimized fp16 model, optimized fp32 model, raw model
    onnx_model_path = os.path.join(onnx_dir, model_name + ".onnx")
    optimized_fp32_model = os.path.join(onnx_dir, model_name + "_fp32.onnx")
    optimized_fp16_model = os.path.join(onnx_dir, model_name + "_fp16.onnx")
    if os.path.isfile(optimized_fp16_model):
        onnx_model_path = optimized_fp16_model
    elif os.path.isfile(optimized_fp32_model):
        onnx_model_path = optimized_fp32_model
    return onnx_model_path

