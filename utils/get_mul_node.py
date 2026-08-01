
def get_mul_node(inputs, output, name):
    """
    Helper function to create a Mul node.
        parameter inputs: list of input names.
        parameter output: output name.
        parameter name: name of the node.
        return: Mul node in NodeProto format.
    """
    return onnx.helper.make_node("Mul", inputs, [output], name)

