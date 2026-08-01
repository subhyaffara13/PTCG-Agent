
def adapt_fp_quant_config(config: FPQuantConfig):
    if config.forward_dtype == "mxfp4":
        forward_dtype = FPQuantDtype.MXFP4
    elif config.forward_dtype == "nvfp4":
        forward_dtype = FPQuantDtype.NVFP4
    else:
        raise ValueError(f"Unsupported forward dtype: {config.forward_dtype}")

    if config.backward_dtype == "bf16":
        backward_dtype = FPQuantDtype.BF16
    elif config.backward_dtype == "mxfp8":
        backward_dtype = FPQuantDtype.MXFP8
    elif config.backward_dtype == "mxfp4":
        backward_dtype = FPQuantDtype.MXFP4
    else:
        raise ValueError(f"Unsupported backward dtype: {config.backward_dtype}")

    return FPQuantLinearConfig(
        forward_dtype=forward_dtype,
        forward_method=config.forward_method,
        backward_dtype=backward_dtype,
        store_master_weights=config.store_master_weights,
        hadamard_group_size=config.hadamard_group_size,
        pseudoquantization=config.pseudoquantization,
        transform_init=config.transform_init,
        modules_to_not_convert=config.modules_to_not_convert,
    )

