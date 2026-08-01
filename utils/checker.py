
def checker(model_path: pathlib.Path, logger: logging.Logger):
    model_with_shape_info_wrapper = ModelProtoWithShapeInfo(model_path)
    model_with_shape_info = model_with_shape_info_wrapper.model_with_shape_info

    dynamic_inputs, num_dynamic_values = check_shapes(model_with_shape_info.graph)

    def check_ep(ep_name, checker_func):
        logger.info(f"Checking {ep_name}")

        # check with shape info first so supported nodes takes into account values with dynamic shapes
        require_fixed_input_sizes = True
        partition_info = checker_func(model_with_shape_info, require_fixed_input_sizes)
        if logger.getEffectiveLevel() <= logging.INFO:
            partition_info.print_analysis(logger, ep_name)

        suitability = partition_info.suitability()
        logger.info(f"Model should perform well with {ep_name} as is: {suitability.name}")

        if suitability != PartitioningInfo.TryWithEP.YES and dynamic_inputs:
            logger.info("--------")
            logger.info("Checking if model will perform better if the dynamic shapes are fixed...")
            require_fixed_input_sizes = False
            partition_info_with_fixed_shapes = checker_func(model_with_shape_info, require_fixed_input_sizes)

            if logger.getEffectiveLevel() <= logging.INFO:
                # analyze and log detailed info
                logger.info("Partition information if the model was updated to make the shapes fixed:")
                partition_info_with_fixed_shapes.print_analysis(logger, ep_name)

            fixed_shape_suitability = partition_info_with_fixed_shapes.suitability()
            logger.info(
                f"Model should perform well with {ep_name} if modified to have fixed input shapes: "
                f"{fixed_shape_suitability.name}"
            )

            if fixed_shape_suitability != PartitioningInfo.TryWithEP.NO:
                logger.info("Shapes can be altered using python -m onnxruntime.tools.make_dynamic_shape_fixed")

            if fixed_shape_suitability.value > suitability.value:
                suitability = fixed_shape_suitability

        logger.info("================")
        logger.info("")

        return suitability

    nnapi_suitability = check_ep("NNAPI", check_nnapi_partitions)

    # Check for NeuralNetwork CoreML model
    def check_nn_coreml(model: onnx.ModelProto, require_fixed_input_sizes):
        return check_coreml_partitions(model, require_fixed_input_sizes, "coreml_supported_neuralnetwork_ops.md")

    # Check for MLProgram CoreML model
    def check_mlprogram_coreml(model: onnx.ModelProto, require_fixed_input_sizes):
        return check_coreml_partitions(model, require_fixed_input_sizes, "coreml_supported_mlprogram_ops.md")

    coreml_nn_suitability = check_ep("CoreML NeuralNetwork", check_nn_coreml)
    coreml_mlprogram_suitability = check_ep("CoreML MLProgram", check_mlprogram_coreml)

    if (
        nnapi_suitability != PartitioningInfo.TryWithEP.YES
        or coreml_nn_suitability != PartitioningInfo.TryWithEP.YES
        or coreml_mlprogram_suitability != PartitioningInfo.TryWithEP.YES
    ) and logger.getEffectiveLevel() > logging.INFO:
        logger.info("Re-run with log level of INFO for more details on the NNAPI/CoreML issues.")

    return (
        nnapi_suitability != PartitioningInfo.TryWithEP.NO
        or coreml_nn_suitability != PartitioningInfo.TryWithEP.NO
        or coreml_mlprogram_suitability != PartitioningInfo.TryWithEP.NO
    )

