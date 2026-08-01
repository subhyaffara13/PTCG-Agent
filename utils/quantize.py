
def quantize(model, run_fn, run_args, mapping=None, inplace=False):
    r"""Quantize the input float model with post training static quantization.

    First it will prepare the model for calibration, then it calls
    `run_fn` which will run the calibration step, after that we will
    convert the model to a quantized model.

    Args:
        model: input float model
        run_fn: a calibration function for calibrating the prepared model
        run_args: positional arguments for `run_fn`
        inplace: carry out model transformations in-place, the original module is mutated
        mapping: correspondence between original module types and quantized counterparts

    Return:
        Quantized model.
    """
    torch._C._log_api_usage_once("quantization_api.quantize.quantize")
    if mapping is None:
        mapping = get_default_static_quant_module_mappings()
    if not inplace:
        model = copy.deepcopy(model)
    model.eval()
    prepare(model, inplace=True)
    run_fn(model, *run_args)
    convert(model, mapping, inplace=True)
    return model


def quantize(
    model_input: str | Path | onnx.ModelProto,
    model_output: str | Path,
    quant_config: QuantConfig,
):
    """Quantize a model with QuantConfig.

    Args:
        model_input (str | Path | ModelProto): Path to the model or ModelProto to quantize.
        model_output (str | Path): Path to save the quantized model.
        quant_config (QuantConfig | WeightOnlyQuantConfig): Quantization Configuration.
    """
    if isinstance(quant_config, StaticQuantConfig):
        quantize_static(
            model_input,
            model_output,
            quant_config.calibration_data_reader,
            calibrate_method=quant_config.calibrate_method,
            quant_format=quant_config.quant_format,
            activation_type=quant_config.activation_type,
            weight_type=quant_config.weight_type,
            op_types_to_quantize=quant_config.op_types_to_quantize,
            nodes_to_quantize=quant_config.nodes_to_quantize,
            nodes_to_exclude=quant_config.nodes_to_exclude,
            per_channel=quant_config.per_channel,
            reduce_range=quant_config.reduce_range,
            use_external_data_format=quant_config.use_external_data_format,
            calibration_providers=quant_config.calibration_providers,
            extra_options=quant_config.extra_options,
        )

    elif isinstance(quant_config, DynamicQuantConfig):
        quantize_dynamic(
            model_input,
            model_output,
            weight_type=quant_config.weight_type,
            op_types_to_quantize=quant_config.op_types_to_quantize,
            nodes_to_quantize=quant_config.nodes_to_quantize,
            nodes_to_exclude=quant_config.nodes_to_exclude,
            per_channel=quant_config.per_channel,
            reduce_range=quant_config.reduce_range,
            use_external_data_format=quant_config.use_external_data_format,
            extra_options=quant_config.extra_options,
        )
    else:
        # training package doesn't has quantize_matmul_4bits, avoid global import
        from .matmul_nbits_quantizer import MatMulNBitsQuantizer, WeightOnlyQuantConfig  # noqa: PLC0415

        if isinstance(quant_config, WeightOnlyQuantConfig):
            model = model_input if isinstance(model_input, onnx.ModelProto) else onnx.load(model_input)
            quant = MatMulNBitsQuantizer(model, algo_config=quant_config)
            quant.process()
            quant.model.save_model_to_file(model_output, True)
        else:
            raise TypeError(
                "Invalid quantization config type, it must be either StaticQuantConfig, "
                "DynamicQuantConfig, or WeightOnlyQuantConfig."
            )


def quantize(x, config):
  x_shape = x.shape
  contract_dim = x_shape[-1]
  block_size = config.block_size
  assert contract_dim >= block_size and contract_dim % block_size == 0
  x_new_shape = x_shape[:-1] + (x_shape[-1] // block_size, block_size)
  x = x.reshape(x_new_shape)  # shape = (B, M, K / block_size, block_size)
  MAX = dtypes.finfo(config.data_type).max.astype(x.dtype)

  def get_scales_per_block(values):
    # shape = (B, M, K / block_size, 1)
    return jnp.max(jnp.abs(values), axis=-1, keepdims=True) / MAX

  if config.mode == "mxfp8":
    assert config.global_scale is None
    assert config.scale_type == dtypes.float8_e8m0fnu

    scales_q = cast_to_e8m0_with_rounding_up(get_scales_per_block(x))
    scaled_x = x / e8m0_to_dtype(scales_q, x.dtype)
  elif config.mode == "nvfp4":
    assert config.scale_type == dtypes.float8_e4m3fn
    assert config.global_scale.dtype == np.float32

    SCALE_MAX = dtypes.finfo(config.scale_type).max.astype(x.dtype)

    x /= config.global_scale
    scales_q = jnp.clip(get_scales_per_block(x), 0, SCALE_MAX)
    scales_q = lax.optimization_barrier(scales_q.astype(config.scale_type))
    scaled_x = x / scales_q.astype(np.float32)
  else:
    raise ValueError(f"Unrecognized mode: {config.mode}.")

  clipped_x = jnp.clip(scaled_x, -MAX, MAX)
  x_q = clipped_x.astype(config.data_type)

  x_q = x_q.reshape(x_shape)  # shape = (B, M, K)
  scales_q = jnp.reshape(scales_q, scales_q.shape[:-1]).view(
      config.scale_type
  )
  return x_q, scales_q


def quantize(x, q_dtype, scale, compute_dtype):
  # Explicitly cast the max values to the compute dtype to avoid unnecessary
  # casting to FP32 during the subsequent math operations."
  dtype_max = get_fp8_max(q_dtype, compute_dtype)
  scaled_x = x / jnp.broadcast_to(scale.astype(compute_dtype), x.shape)
  clipped_x = jnp.clip(scaled_x, -dtype_max, dtype_max)
  return clipped_x.astype(q_dtype)

