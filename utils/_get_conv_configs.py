
def _get_conv_configs() -> list[BackendPatternConfig]:
    """
    Return all configs related to conv modules and ops.
    """
    observation_type = ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT
    dtype_configs = [
        qnnpack_weighted_op_qint8_symmetric_dtype_config,
        executorch_weighted_op_int8_dtype_config,
    ]
    conv_configs = []
    for convs in [_Conv2dMetadata]:
        # (1) Single conv modules/functions
        # -----------------------------------
        # conv module
        conv_configs.append(
            BackendPatternConfig(convs.root)
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
            .set_root_module(convs.root)
            .set_reference_quantized_module(convs.reference)
            .set_qat_module(convs.qat)
        )
        # conv qat module
        conv_configs.append(
            BackendPatternConfig(convs.qat)
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
            .set_root_module(convs.root)
            .set_reference_quantized_module(convs.reference)
        )
        # functional conv
        conv_configs.append(
            BackendPatternConfig(convs.func)
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
            ._set_input_type_to_index({"weight": 1, "bias": 2})
        )

        # (2) Conv + relu
        # -----------------------------------
        # conv module + relu module
        conv_configs.append(
            BackendPatternConfig((convs.root, nn.ReLU))
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_fuser_method(_sequential_wrapper2(convs.fused_conv_relu))
            .set_fused_module(convs.fused_conv_relu)
        )
        # conv module + functional relu
        conv_configs.append(
            BackendPatternConfig((convs.root, F.relu))
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_fuser_method(_sequential_wrapper2(convs.fused_conv_relu))
            .set_fused_module(convs.fused_conv_relu)
        )
        # fused conv relu module
        conv_configs.append(
            BackendPatternConfig(convs.fused_conv_relu)
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
            .set_root_module(convs.root)
            .set_reference_quantized_module(convs.reference)
            .set_qat_module(convs.relu_qat)
        )
        # conv relu, qat fused module
        conv_configs.append(
            BackendPatternConfig(convs.relu_qat)
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
            .set_root_module(convs.root)
            .set_reference_quantized_module(convs.reference)
        )
        # functional conv + relu module
        conv_configs.append(
            BackendPatternConfig((convs.func, nn.ReLU))
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
        )
        # functional conv + functional relu
        conv_configs.append(
            BackendPatternConfig((convs.func, F.relu))
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
        )
        # fused conv relu
        conv_configs.append(
            BackendPatternConfig(convs.fused_conv_relu)
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_qat_module(convs.relu_qat)
        )

        conv_configs.append(
            BackendPatternConfig(convs.relu_qat)
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_root_module(convs.root)
            .set_reference_quantized_module(convs.reference)
        )

        # (3) Conv + batchnorm (+ relu)
        # -------------------------------
        # conv + batchnorm (+ relu)
        conv_configs.append(
            BackendPatternConfig((convs.root, convs.bn))
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_fuser_method(fuse_conv_bn)
            .set_fused_module(convs.fused_conv_bn)
        )
        # conv + bn + relu module fusion
        conv_configs.append(
            BackendPatternConfig((convs.root, convs.bn, nn.ReLU))
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_fuser_method(fuse_conv_bn_relu)
            .set_fused_module(convs.fused_conv_bn_relu)
        )
        # conv + bn + relu functional fusion
        conv_configs.append(
            BackendPatternConfig((convs.root, convs.bn, F.relu))
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_root_module(convs.root)
            .set_fuser_method(fuse_conv_bn_relu)
            .set_fused_module(convs.fused_conv_bn_relu)
        )
        # TODO: we can add fusion for torch.relu as well
        # 3.2 conv + bn (+ relu) fused module configs
        # fused conv bn
        conv_configs.append(
            BackendPatternConfig(convs.fused_conv_bn)
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_qat_module(convs.bn_qat)
        )

        # fused conv bn relu
        conv_configs.append(
            BackendPatternConfig(convs.fused_conv_bn_relu)
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_qat_module(convs.bn_relu_qat)
        )

        # conv bn, qat fused module
        conv_configs.append(
            BackendPatternConfig(convs.bn_qat)
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
            .set_root_module(convs.root)
            .set_reference_quantized_module(convs.reference)
        )
        # conv bn relu, qat fused module
        conv_configs.append(
            BackendPatternConfig(convs.bn_relu_qat)
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
            .set_root_module(convs.root)
            .set_reference_quantized_module(convs.reference)
        )
    return conv_configs


def _get_conv_configs(dtype_configs):
    """
    Return all configs related to conv modules and ops.
    """
    conv_configs = []
    observation_type = ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT
    for convs in [_Conv1dMetadata, _Conv2dMetadata, _Conv3dMetadata]:
        # (1) Single conv modules/functions
        # -----------------------------------
        # conv module
        conv_configs.append(
            BackendPatternConfig(convs.root)
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
            .set_root_module(convs.root)
            .set_reference_quantized_module(convs.reference)
            .set_qat_module(convs.qat)
        )
        # conv qat module
        conv_configs.append(
            BackendPatternConfig(convs.qat)
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
            .set_root_module(convs.root)
            .set_reference_quantized_module(convs.reference)
        )
        # functional conv
        conv_configs.append(
            BackendPatternConfig(convs.func)
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
            ._set_input_type_to_index({"weight": 1, "bias": 2})
        )

        # (2) Conv + relu
        # -----------------
        # 2.1 conv module + relu fusion configs
        # conv relu fusion, conv module + relu module
        conv_configs.append(
            BackendPatternConfig((convs.root, torch.nn.ReLU))
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_fuser_method(_sequential_wrapper2(convs.fused_conv_relu))
            .set_fused_module(convs.fused_conv_relu)
        )
        # conv relu fusion, conv module + functional relu
        conv_configs.append(
            BackendPatternConfig((convs.root, F.relu))
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_fuser_method(_sequential_wrapper2(convs.fused_conv_relu))
            .set_fused_module(convs.fused_conv_relu)
        )
        # 2.2 conv module + relu fused module configs
        # conv relu, fused module
        conv_configs.append(
            BackendPatternConfig(convs.fused_conv_relu)
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
            .set_root_module(convs.root)
            .set_reference_quantized_module(convs.reference)
            .set_qat_module(convs.relu_qat)
        )
        # conv relu, qat fused module
        conv_configs.append(
            BackendPatternConfig(convs.relu_qat)
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
            .set_root_module(convs.root)
            .set_reference_quantized_module(convs.reference)
        )
        # 2.3 functional conv + relu configs
        # conv relu, functional conv + relu module
        conv_configs.append(
            BackendPatternConfig((convs.func, torch.nn.ReLU))
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
        )
        # conv relu, functional conv + functional relu
        conv_configs.append(
            BackendPatternConfig((convs.func, F.relu))
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
        )

        # fused conv relu
        conv_configs.append(
            BackendPatternConfig(convs.fused_conv_relu)
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_qat_module(convs.relu_qat)
        )

        conv_configs.append(
            BackendPatternConfig(convs.relu_qat)
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_root_module(convs.root)
            .set_reference_quantized_module(convs.reference)
        )

        # (3) Conv + batchnorm (+ relu)
        # -------------------------------
        # 3.1 conv bn fusion configs
        # conv + bn fusion
        conv_configs.append(
            BackendPatternConfig((convs.root, convs.bn))
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_fuser_method(fuse_conv_bn)
            .set_fused_module(convs.fused_conv_bn)
        )
        # conv + bn + relu module fusion
        conv_configs.append(
            BackendPatternConfig((convs.root, convs.bn, nn.ReLU))
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_fuser_method(fuse_conv_bn_relu)
            .set_fused_module(convs.fused_conv_bn_relu)
        )
        # conv + bn + relu functional fusion
        conv_configs.append(
            BackendPatternConfig((convs.root, convs.bn, F.relu))
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_root_module(convs.root)
            .set_fuser_method(fuse_conv_bn_relu)
            .set_fused_module(convs.fused_conv_bn_relu)
        )
        # TODO: we can add fusion for torch.relu as well

        # 3.2 conv + bn (+ relu) fused module configs
        # fused conv bn
        conv_configs.append(
            BackendPatternConfig(convs.fused_conv_bn)
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_qat_module(convs.bn_qat)
        )

        # fused conv bn relu
        conv_configs.append(
            BackendPatternConfig(convs.fused_conv_bn_relu)
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_qat_module(convs.bn_relu_qat)
        )

        # conv bn, qat fused module
        conv_configs.append(
            BackendPatternConfig(convs.bn_qat)
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
            .set_root_module(convs.root)
            .set_reference_quantized_module(convs.reference)
        )
        # conv bn relu, qat fused module
        conv_configs.append(
            BackendPatternConfig(convs.bn_relu_qat)
            .set_observation_type(observation_type)  # noqa: E131
            .set_dtype_configs(dtype_configs)
            .set_root_module(convs.root)
            .set_reference_quantized_module(convs.reference)
        )

        # (4) conv transpose and its fusion
        # 4.1 conv transpose config
        conv_configs.append(
            BackendPatternConfig(convs.transpose)
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_root_module(convs.transpose)
            .set_reference_quantized_module(convs.transpose_reference)
        )

        # 4.2 conv transpose + bn fusion
        conv_configs.append(
            BackendPatternConfig((convs.transpose, convs.bn))
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_fuser_method(fuse_convtranspose_bn)
            .set_root_module(convs.transpose)
            .set_reference_quantized_module(convs.transpose_reference)
        )

        # 4.3 functional conv transpose
        conv_configs.append(
            BackendPatternConfig(convs.func_transpose)
            .set_dtype_configs(dtype_configs)  # noqa: E131
            ._set_input_type_to_index({"weight": 1, "bias": 2})
        )

    return conv_configs

