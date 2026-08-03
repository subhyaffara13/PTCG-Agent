from pathlib import Path


def load_model_with_shape_infer(model_path: Path) -> ModelProto:
    inferred_model_path = generate_identified_filename(model_path, "-inferred")
    onnx.shape_inference.infer_shapes_path(str(model_path), str(inferred_model_path))
    model = onnx.load(inferred_model_path.as_posix())
    add_infer_metadata(model)
    inferred_model_path.unlink()
    return model

