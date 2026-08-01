
def fix_output_shapes(model: onnx.ModelProto):
    """
    Update the output shapesof a model where the input shape/s were made fixed, if possible.
    This is mainly to make the model usage clearer if the output shapes can be inferred from the new input shapes.
    :param model: Model that had input shapes fixed.
    """

    # get a version of the model with shape inferencing info in it. this will provide fixed output shapes if possible.
    m2 = onnx.shape_inference.infer_shapes(model)
    onnx.checker.check_model(m2)

    for idx, o in enumerate(model.graph.output):
        if not is_fixed_size_tensor(o):
            new_o = m2.graph.output[idx]
            if is_fixed_size_tensor(new_o):
                o.type.tensor_type.shape.CopyFrom(new_o.type.tensor_type.shape)

