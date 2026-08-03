import logging

def update_opset_version(
    model: ModelProto,
    weight_type: QuantType,
    activation_type: QuantType | None = None,
    tensor_quant_overrides: dict | None = None,
    block_size: int = 0,
) -> ModelProto:
    opset_version = get_opset_version(model)
    target_opset_version = opset_version
    weight_quant_type = getattr(weight_type, "tensor_type", weight_type)
    activation_quant_type = (
        getattr(activation_type, "tensor_type", activation_type) if activation_type is not None else None
    )

    _int16_types = (onnx.TensorProto.UINT16, onnx.TensorProto.INT16)
    needs_opset21_for_16bit = weight_quant_type in _int16_types or activation_quant_type in _int16_types

    # Also check TensorQuantOverrides for any 16-bit types, including per-override convert.quant_type.
    # Validation of structure is deferred to TensorQuantOverridesHelper.is_valid(); skip bump heuristic on malformed input.
    if not needs_opset21_for_16bit and tensor_quant_overrides:
        _int16_quant_types = {QuantType.QInt16, QuantType.QUInt16}
        try:
            for overrides_list in tensor_quant_overrides.values():
                for override in overrides_list:
                    qt = override.get("quant_type")
                    if qt in _int16_quant_types:
                        needs_opset21_for_16bit = True
                        break
                    convert = override.get("convert")
                    if convert is not None:
                        convert_qt = convert.get("quant_type")
                        if convert_qt in _int16_quant_types:
                            needs_opset21_for_16bit = True
                            break
                if needs_opset21_for_16bit:
                    break
        except (AttributeError, TypeError):
            # Malformed overrides; structural validation is deferred to
            # TensorQuantOverridesHelper.is_valid(). Skip bump heuristic.
            logging.debug("Skipping 16-bit opset bump heuristic for TensorQuantOverrides: structure not as expected.")

    if opset_version < 21 and block_size > 0:
        logging.warning(
            f"The original model opset version is {opset_version}, which does not support block-wise "
            "quantization natively. "
            "Please update the model to opset >= 21. Automatically updating the model to opset 21. "
            "Please verify the quantized model."
        )
        target_opset_version = 21

    elif opset_version < 19 and weight_quant_type == onnx.TensorProto.FLOAT8E4M3FN:
        logging.warning(
            f"The original model opset version is {opset_version}, which does not support quantization to float 8. "
            "Please update the model to opset >= 19. Automatically update the model to opset 19. "
            "Please verify the quantized model."
        )
        target_opset_version = 19

    elif opset_version < 21 and needs_opset21_for_16bit:
        logging.warning(
            f"The original model opset version is {opset_version}, which does not support 16-bit integer "
            "quantization natively. "
            "Please update the model to opset >= 21. Automatically update the model to opset 21. "
            "Please verify the quantized model."
        )
        target_opset_version = 21

    elif opset_version == 10:
        logging.warning(
            f"The original model opset version is {opset_version}, which does not support node fusions. "
            "Please update the model to opset >= 11 for better performance."
        )

    elif opset_version < 10:
        logging.warning(
            f"The original model opset version is {opset_version}, which does not support quantization. "
            "Please update the model to opset >= 11. Automatically update the model to opset 11. "
            "Please verify the quantized model."
        )
        target_opset_version = 11

    if target_opset_version != opset_version:
        model = onnx.version_converter.convert_version(model, target_opset_version)
        # Additional nodes may be added to the model during the opset version conversion. Run shape inference
        # to ensure all nodes are included in model.graph.value_info.
        model = save_and_reload_model_with_shape_infer(model)

    return model

