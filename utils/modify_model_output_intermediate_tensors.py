
def modify_model_output_intermediate_tensors(
    input_model_path: str | Path,
    output_model_path: str | Path,
    op_types_for_saving: Sequence[str] | None = None,
    save_as_external_data: bool = False,
) -> None:
    """Augment a given ONNX model to save node input/output tensors.

    Add all input/output tensors of operator nodes to model outputs
    so that their values can be retrieved for debugging purposes.

    Args:
        input_model: the path to load the model.
        op_types_for_saving: Operator types for which the
                input/output should be saved. By default, saving all the
                float32/float16 tensors.

    Returns:
        The augmented ONNX model
    """

    if op_types_for_saving is None:
        op_types_for_saving = []
    saver = CalibraterBase(input_model_path, op_types_to_calibrate=op_types_for_saving)
    model_to_augment = saver.model
    tensors, value_infos = saver.select_tensors_to_calibrate(model_to_augment)
    reshape_shape_name = "LinearReshape_" + str(time.time())
    reshape_shape = numpy_helper.from_array(numpy.array([-1], dtype=numpy.int64), reshape_shape_name)
    model_to_augment.graph.initializer.append(reshape_shape)

    for tensor_name in tensors:
        reshape_output = tensor_name + _TENSOR_SAVE_POSTFIX
        reshape_node = onnx.helper.make_node(
            "Reshape",
            inputs=[tensor_name, reshape_shape_name],
            outputs=[reshape_output],
            name=reshape_output,
        )
        model_to_augment.graph.node.append(reshape_node)
        reshape_output_value_info = helper.make_tensor_value_info(
            reshape_output, value_infos[tensor_name].type.tensor_type.elem_type, [-1]
        )
        model_to_augment.graph.output.append(reshape_output_value_info)

    onnx.save(
        model_to_augment,
        output_model_path,
        save_as_external_data=save_as_external_data,
    )

