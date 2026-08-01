
def get_fusion_statistics(optimized_model_path: str) -> dict[str, int]:
    """
    Get counter of fused operators in optimized model.

    Args:
        optimized_model_path (str): the path of onnx model.

    Returns:
        A dictionary with operator type as key, and count as value
    """
    model = load_model(optimized_model_path, format=None, load_external_data=True)
    optimizer = BertOnnxModel(model)
    return optimizer.get_fused_operator_statistics()

