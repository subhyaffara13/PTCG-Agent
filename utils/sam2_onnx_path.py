
def sam2_onnx_path(output_dir, model_type, component, multimask_output=False, suffix=""):
    if component == "image_encoder":
        return os.path.join(output_dir, f"{model_type}_image_encoder{suffix}.onnx")
    elif component == "mask_decoder":
        return os.path.join(output_dir, f"{model_type}_mask_decoder{suffix}.onnx")
    elif component == "prompt_encoder":
        return os.path.join(output_dir, f"{model_type}_prompt_encoder{suffix}.onnx")
    else:
        assert component == "image_decoder"
        return os.path.join(
            output_dir, f"{model_type}_image_decoder" + ("_multi" if multimask_output else "") + f"{suffix}.onnx"
        )

