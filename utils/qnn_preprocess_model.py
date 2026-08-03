import logging
from pathlib import Path


def qnn_preprocess_model(
    model_input: str | pathlib.Path | onnx.ModelProto,
    model_output: str | pathlib.Path,
    fuse_layernorm: bool = False,
    save_as_external_data: bool = False,
    all_tensors_to_one_file: bool = False,
    external_data_location: str | None = None,
    external_data_size_threshold: int = 1024,
    external_data_convert_attribute: bool = False,
    inputs_to_make_channel_last: list[str] | None = None,
    outputs_to_make_channel_last: list[str] | None = None,
    dynamic_input_shapes: list[tuple[str, str]] | None = None,
    exclude_initializer_from_input: bool = False,
) -> bool:
    """Preprocess ONNX model for QNN.

    Args:
        model_input: A path or ONNX ModelProto specifiying the model to be preprocessed.
        model_output: A path specifying where the preprocessed model to be saved.
        fuse_layernorm: A bool specifying whether to fuse the matched sequence into a single LayerNormalization node.
            Defaults to False.
        save_as_external_data: A bool specifying whether to save model with external data. Defaults to False.
        all_tensors_to_one_file: A bool specifying whether to save all external data in one file or save each tensor to
            a file named with the tensor name. This argument is effective only when `save_as_external_data` is True.
            Defaults to False.
        external_data_location: A str specifying where to save the external data. The path is relative to the model
            path. This argument is effective only when `save_as_external_data` is True. Defaults to the model name.
        external_data_size_threshold: An int specifying the threshold of data size for tensors be saved as external
            data. This argument is effective only when `save_as_external_data` is True. Defaults to 1024.
        external_data_convert_attribute: A bool specifying whether to save all tensors including attributes as external
            data. This argument is effective only when `save_as_external_data` is True. Defaults to False.
        inputs_to_make_channel_last: A list of strs specifying graph input names to be transposed into channel-last.
            Defaults to None.
        outputs_to_make_channel_last: A list of strs specifying graph output names to be transposed into channel-last.
            Defaults to None.
        dynamic_input_shapes: A list of tuples specifying model input name to and its static shape in comma seprated
            format, for example: [('input', '1,3,256,256')]. Defaults to None.
        exclude_initializer_from_input: A bool specifying whether to exclude initializer from input. Defaults to False.

    Returns:
        A bool indicating whether the model is modified.
    """
    return qnn.qnn_preprocess_model(
        model_input,
        model_output,
        fuse_layernorm=fuse_layernorm,
        save_as_external_data=save_as_external_data,
        all_tensors_to_one_file=all_tensors_to_one_file,
        external_data_location=external_data_location,
        external_data_size_threshold=external_data_size_threshold,
        external_data_convert_attribute=external_data_convert_attribute,
        inputs_to_make_channel_last=inputs_to_make_channel_last,
        outputs_to_make_channel_last=outputs_to_make_channel_last,
        dynamic_input_shapes=dynamic_input_shapes,
        exclude_initializer_from_input=exclude_initializer_from_input,
    )


def qnn_preprocess_model(
    model_input: str | Path | onnx.ModelProto,
    model_output: str | Path,
    exclude_initializer_from_input: bool = False,
    fuse_layernorm: bool = False,
    save_as_external_data: bool = False,
    all_tensors_to_one_file: bool = False,
    external_data_location: str | None = None,
    external_data_size_threshold: int = 1024,
    external_data_convert_attribute: bool = False,
    inputs_to_make_channel_last: list[str] | None = None,
    outputs_to_make_channel_last: list[str] | None = None,
    dynamic_input_shapes: list[tuple[str, str]] | None = None,
) -> bool:
    """
    If necessary, this method creates a new "pre-processed" model in preparation for
    quantization of a model to be used in QNN EP. Returns true if a new model was created.

    This method perfoms the following operations:
    - Fuse Erf sequence into a single Gelu node.
    - Fuse ReduceL2 sequence into a single LpNormalization node (p == 2).
    - (Optional) Fuse ReduceMean sequence into a single LayerNormalization node.

    Args:
        model_input: Path to the input model file or ModelProto.
        model_output: Path the output model file, which is only created if this method returns True.
        exclude_initializer_from_input: A bool specifying whether to exclude initializer from input.
            Defaults to False.
        fuse_layernorm: True if ReduceMean sequences should be fused into LayerNormalization nodes.
            Defaults to False.
        save_as_external_data: True if output model should be saved with external data. Defaults to false.
        all_tensors_to_one_file: Effective only if save_as_external_data is true. Defaults to false.
            If true, save all tensors to one external file specified by external_data_location.
            If false, save each tensor to a file named with the tensor name.
        external_data_location: Effective only if save_as_external_data is true. Defaults to None.
            Specify the external file to which all tensors are saved. Path is relative
            to the model path. If not specified, the model's name is used.
        external_data_size_threshold: Effective only if save_as_external_data is true. Defaults to 1024.
            Tensors with a data size >= external_data_size_threshold are converted to external data.
            To convert every tensor with raw data to external data, set to 0.
        external_data_convert_attribute: Effective only if save_as_external_data is true. Defaults to false.
            If true, convert all tensors to external data.
            If false, convert only non-attribute tensors to external data.
        inputs_to_make_channel_last: List of graph input names to transpose to be "channel-last". For example,
            if "input0" originally has the shape (N, C, D1, D2, ..., Dn), the resulting model will change input0's
            shape to (N, D1, D2, ..., Dn, C) and add a transpose node after it.

            Original:
                input0 (N, C, D1, D2, ..., Dn) --> <Nodes>

            Updated:
                input0 (N, D1, D2, ..., Dn, C) --> Transpose --> input0_chanfirst (N, C, D1, D2, ..., Dn) --> <Nodes>

            This can potentially improve inference latency for QDQ models running on QNN EP because the
            additional transpose node may allow other transpose nodes inserted during ORT layout transformation
            to cancel out.
        outputs_to_make_channel_last: List of graph output names to transpose to be "channel-last". For example,
            if "output0" originally has the shape (N, C, D1, D2, ..., Dn), the resulting model will change output0's
            shape to (N, D1, D2, ..., Dn, C) and add a transpose node before it.

            Original:
                <Nodes> --> output0 (N, C, D1, D2, ..., Dn)

            Updated:
                <Nodes> --> output0_chanfirst (N, C, D1, D2, ..., Dn) --> Transpose --> output0 (N, D1, D2, ..., Dn, C)

            This can potentially improve inference latency for QDQ models running on QNN EP because the
            additional transpose node may allow other transpose nodes inserted during ORT layout transformation
            to cancel out.
        dynamic_input_shapes: A list of tuples specifying model input name to and its static shape in comma seprated
            format, for example: [('input', '1,3,256,256')]. Defaults to None.
    """
    modified = False
    model = model_input if isinstance(model_input, onnx.ModelProto) else onnx.load_model(model_input)
    model = save_and_reload_optimize_model(model, shape_infer=True)
    onnx_model = ONNXModel(model)

    # Optionally, fix the dynamic input shapes.
    if dynamic_input_shapes:
        for input_name, input_shape_str in dynamic_input_shapes:
            input_shape = [int(i) for i in input_shape_str.split(",")]
            make_input_shape_fixed(onnx_model.graph(), input_name, input_shape)
        fix_output_shapes(onnx_model.model)
        modified = True

    # Exclude initializer from input if model.ir_version >= 4
    if exclude_initializer_from_input:
        modified |= remove_initializer_from_input(onnx_model.model)

    # Fuse Erf sequence into a single Gelu
    fusion_gelu = FusionGelu(onnx_model)
    if fusion_gelu.apply():
        modified = True

    # Fuse ReduceL2 sequence into a single LpNormalization node with p == 2.
    fusion_lpnorm = FusionLpNormalization(onnx_model)
    if fusion_lpnorm.apply():
        modified = True

    # Fuse Reshape/Transpose sequence into a single SpaceToDepth.
    fusion_s2d = FusionSpaceToDepth(onnx_model)
    if fusion_s2d.apply():
        modified = True

    # Optionally, fuse ReduceMean sequence into a single LayerNormalization node.
    if fuse_layernorm:
        onnx_opset = next(x for x in model.opset_import if x.domain == "" or x.domain == "ai.onnx")

        # Need opset >= 17 to use LayerNormalization.
        if onnx_opset.version < 17:
            logging.warning(
                "Unable to fuse ReduceMean sequence into a LayerNormalization node. "
                "ONNX model must use an opset >= 17 in order to use LayerNormalization, "
                f"but found version {onnx_opset.version}. Please use onnx.version_converter to update your model."
            )
        else:
            fusion_layernorm = FusionLayerNormalization(onnx_model)
            if fusion_layernorm.apply():
                modified = True

    # Optionally, transpose inputs and/or outputs to make them "channel-last".
    if inputs_to_make_channel_last or outputs_to_make_channel_last:
        transpose_node_prefix = "Transpose_channel_"
        transpose_node_suffix: int = onnx_model.get_largest_node_name_suffix(transpose_node_prefix) + 1
        update_io_to_channel_last(
            onnx_model.model,
            inputs_to_make_channel_last,
            outputs_to_make_channel_last,
            transpose_node_name_prefix=transpose_node_prefix,
            transpose_node_name_start_suffix=transpose_node_suffix,
        )
        modified = True

    # Make sure all nodes have a name.
    unnamed_node_prefix = "qnn_preproc_node_"
    available_suffix = onnx_model.get_largest_node_name_suffix(unnamed_node_prefix) + 1
    for node in onnx_model.model.graph.node:
        if node.op_type != "Constant" and not node.name:
            new_node_name = f"{unnamed_node_prefix}{available_suffix!s}"
            available_suffix += 1
            node.name = new_node_name
            modified = True
            logging.warning(f"Node of type {node.op_type} does not have a name. Renamed to {new_node_name}.")

    if modified:
        onnx_model.topological_sort()
        onnx.save_model(
            model,
            model_output,
            save_as_external_data=save_as_external_data,
            all_tensors_to_one_file=all_tensors_to_one_file,
            location=external_data_location,
            size_threshold=external_data_size_threshold,
            convert_attribute=external_data_convert_attribute,
        )

    return modified

