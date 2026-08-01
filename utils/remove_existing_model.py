
def remove_existing_model(model_path: str):
    # Remove ONNX model and its external data
    data_path = os.path.join(model_path + ".data")
    os.remove(model_path)
    os.remove(data_path)
    logger.warning(f"Removed {model_path} and {data_path}")

