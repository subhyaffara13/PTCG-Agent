import copy
from typing import Any, Callable
from pathlib import Path


def get_qdq_config(
    model_input: str | Path | onnx.ModelProto,
    calibration_data_reader: CalibrationDataReader,
    calibrate_method=CalibrationMethod.MinMax,
    calibrate_args: dict[str, Any] | None = None,
    activation_type=QuantType.QUInt8,
    weight_type=QuantType.QInt8,
    activation_symmetric: bool = False,
    weight_symmetric: bool | None = None,
    per_channel: bool = False,
    reduce_range: bool = False,
    keep_removable_activations: bool = False,
    min_real_range: float | None = None,
    tensor_quant_overrides: dict[str, list[dict[str, Any]]] | None = None,
    calibration_providers: list[str] | None = None,
    op_types_to_quantize: list[str] | None = None,
    nodes_to_exclude: list[str] | Callable[[onnx.ModelProto, onnx.NodeProto], bool] | None = None,
    extra_options: dict | None = None,
) -> StaticQuantConfig:
    """
    Returns a configuration suitable that quantizes the entire model to integer precision.

    Params:
        model_input: Path to the input model file or ModelProto.
        calibration_data_reader: Calibration data reader.
        calibrate_methode: The calibration method. Defaults to MinMax.
        activation_type: The default activation quantization type. Defaults to QUInt8.
        weight_type: The default weight quantization type. Defaults to QInt8.
        activation_symmetric: True if activations should be quantized symmetrically (i.e, rmax == -rmin) by default.
            Defaults to false. For int8 and int16, this results in zero-point values of 0. For uint8 and uint16,
            the zero-point values are 127 and 32,767, respectively.
        weight_symmetric: True if weights should be quantized symmetrically (i.e., rmax == -rmin) by default.
            Defaults to None. If set to None, weight_symmetric is assumed true if a weight's quant type is a signed int.
        per_channel: Global option that determines if a fixed set of operator types should be quantized per-channel.
            Defaults to false. Alternatively, use the tensor-level `tensor_quant_overrides` to select individual operators
            and their quantization axes.
        reduce_range: quantize weights with 1 less bit of precision (e.g., 7 bits for QInt8). Defaults to false.
            May improve the accuracy for some models running on non-VNNI machine, especially for per-channel mode.
        keep_removable_activations: Defaults to false. If true, "removable" activations (e.g., Clip or Relu) will not
                        be removed, and will be explicitly represented in the QDQ model. If false, these activations
                        are automatically removed if activations are asymmetrically quantized. Keeping these activations
                        is necessary if optimizations or EP transformations will later remove
                        QuantizeLinear/DequantizeLinear operators from the model.
        min_real_range: Default is None. If set to a floating-point value, the calculation of the quantization parameters
            (i.e., scale and zero point) will enforce a minimum range between rmin and rmax. If (rmax - rmin)
            is less than the specified minimum range, rmax will be set to rmin + min_real_range.
        tensor_quant_overrides: tensor-level quantization overrides. Defaults to None.
            The key is a tensor name and the value is a list of dictionaries. For per-tensor quantization, the list
            contains a single dictionary. For per-channel quantization, the list contains either a dictionary for
            each channel in the tensor or a single dictionary that is assumed to apply to all channels. An 'axis'
            key must be present in the first dictionary for per-channel quantization.

            Each dictionary contains optional overrides with the following keys and values.
                'quant_type' = QuantType : The tensor's quantization data type.
                'axis' = Int             : The per-channel axis. Must be present for per-channel weights.
                'scale' =  Float         : The scale value to use. Must also specify `zero_point` if set.
                'zero_point' = Int       : The zero-point value to use. Must also specify `scale` is set.
                'symmetric' = Bool       : If the tensor should use symmetric quantization. Invalid if also
                                            set `scale` or `zero_point`.
                'reduce_range' = Bool    : If the quantization range should be reduced. Invalid if also
                                            set `scale` or `zero_point`. Only valid for initializers.
                'rmax' = Float           : Override the maximum real tensor value in calibration data.
                                            Invalid if also set `scale` or `zero_point`.
                'rmin' = Float           : Override the minimum real tensor value in calibration data.
                                            Invalid if also set `scale` or `zero_point`.
                'convert' = Dict         : A nested dictionary with the same keys for an activation
                                           tensor that should be converted to another quantization type.
                'convert["recv_nodes"] = Set : Set of node names that consume the converted activation,
                                               other nodes get the original type. If not specified,
                                               assume all consumer nodes get the converted type.
        calibration_providers: Execution providers to run the session during calibration. Default is None which uses
            [ "CPUExecutionProvider" ].
        op_types_to_quantize: List of operator types to quantize. If None, all operators other than Cast, DequantizeLinear,
            and QuantizeLinear are quantized.
        nodes_to_exclude: List of nodes names to exclude from quantization. Alternatively, can provide a function that
            accepts an onnx.ModelProto and onnx.NodeProto as arguments and returns true if the give onnx.NodeProto
            should be excluded from quantization.
        extra_options: Additional options specified as string key/value pairs. Refer to the documentation for
            `quantize_static` for valid keys and values.

    Returns:
        A StaticQuantConfig object
    """
    q16_types = {QuantType.QInt16, QuantType.QUInt16}
    q4_types = {QuantType.QInt4, QuantType.QUInt4}
    op_types_to_exclude = {"Cast", "DequantizeLinear", "QuantizeLinear"}

    model = (
        model_input
        if isinstance(model_input, onnx.ModelProto)
        else onnx.load_model(model_input, load_external_data=False)
    )

    op_types = set()
    model_has_external_data = False
    overrides_helper = TensorQuantOverridesHelper(
        copy.deepcopy(tensor_quant_overrides) if tensor_quant_overrides else {}
    )

    # check if the model has external data.
    for initializer in model.graph.initializer:
        if onnx.external_data_helper.uses_external_data(initializer):
            model_has_external_data = True

    op_types_to_quantize_set = set(op_types_to_quantize) if op_types_to_quantize else None
    nodes_to_exclude_set = set(nodes_to_exclude) if isinstance(nodes_to_exclude, list) else set()

    # Iterate through nodes to get all operator types in the model and
    # call user's function to filter out nodes from quantization.
    for node in model.graph.node:
        if op_types_to_quantize_set and node.op_type not in op_types_to_quantize_set:
            continue
        if node.name in nodes_to_exclude_set:
            continue
        if callable(nodes_to_exclude) and nodes_to_exclude(model, node):
            nodes_to_exclude_set.add(node.name)
        else:
            op_types.add(node.op_type)

    final_extra_options = {
        "MinimumRealRange": min_real_range,
        "QDQKeepRemovableActivations": keep_removable_activations,
        "ActivationSymmetric": activation_symmetric,
        "WeightSymmetric": weight_symmetric,
        "ForceQuantizeNoInputCheck": True,
        "TensorQuantOverrides": overrides_helper.get_dict(),
    }

    # Pass along known calibration options
    if calibrate_args:
        calib_extra_options_keys = [
            ("symmetric", "CalibTensorRangeSymmetric"),
            ("moving_average", "CalibMovingAverage"),
            ("averaging_constant", "CalibMovingAverageConstant"),
            ("max_intermediate_outputs", "CalibMaxIntermediateOutputs"),
            ("percentile", "CalibPercentile"),
        ]
        calib_extra_options = {
            key: calibrate_args.get(name) for (name, key) in calib_extra_options_keys if name in calibrate_args
        }
        final_extra_options.update(calib_extra_options)

    # ONNX opset < 21 does not support 4-bit quantization natively, so must use 'com.microsoft' domain
    # on Q/DQ operators if using 4-bit quantization.  16-bit weight/activation types are excluded here
    # because quantize_static() will automatically bump the model opset to 21, where native ONNX
    # QuantizeLinear/DequantizeLinear supports INT16/UINT16 and INT4/UINT4 without contrib-domain ops.
    # 16-bit types in TensorQuantOverrides also trigger the same opset bump, so a mixed 16-bit + 4-bit
    # override config will be served at opset 21 where neither type needs contrib ops.
    onnx_opset_version = get_opset_version(model)
    if onnx_opset_version < 21:
        override_types = overrides_helper.get_quant_types()
        overrides_have_16bit = any(t in q16_types for t in override_types)
        # If any 16-bit type is present (top-level or override), quantize_static() will bump the
        # model to opset 21, making contrib ops unnecessary for all types.
        will_bump_to_opset21 = activation_type in q16_types or weight_type in q16_types or overrides_have_16bit
        if not will_bump_to_opset21:
            overrides_have_q4_types = any(t in q4_types for t in override_types)
            needs_contrib_ops = activation_type in q4_types or weight_type in q4_types or overrides_have_q4_types
            if needs_contrib_ops:
                final_extra_options["UseQDQContribOps"] = True

    # Allow user's extra_options to override our final_extra_options.
    if extra_options:
        final_extra_options.update(extra_options)

    return StaticQuantConfig(
        calibration_data_reader,
        calibrate_method=calibrate_method,
        quant_format=QuantFormat.QDQ,
        activation_type=activation_type,
        weight_type=weight_type,
        op_types_to_quantize=(
            op_types_to_quantize if op_types_to_quantize else list(op_types.difference(op_types_to_exclude))
        ),
        nodes_to_exclude=list(nodes_to_exclude_set),
        per_channel=per_channel,
        reduce_range=reduce_range,
        use_external_data_format=(model_has_external_data or model.ByteSize() >= MODEL_SIZE_THRESHOLD),
        calibration_providers=calibration_providers,
        extra_options=final_extra_options,
    )

