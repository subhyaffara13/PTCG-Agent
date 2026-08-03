import os

def remove_existing_files(output_path: str):
    for filename in os.listdir(output_path):
        filepath = os.path.join(output_path, filename)
        if ".onnx" in filename or ".onnx.data" in filename:
            os.remove(filepath)
            logger.warning(f"Removed {filepath}")

