
def get_opsets_imported(model: onnx.ModelProto):
    """
    Get the opsets imported by the model
    :param model: Model to check.
    :return: Map of domain to opset.
    """
    opsets = {}
    for entry in model.opset_import:
        # if empty it's ai.onnx
        domain = entry.domain or "ai.onnx"
        opsets[domain] = entry.version

    return opsets

