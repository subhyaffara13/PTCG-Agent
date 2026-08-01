
def _get_dtype(
    dtype: str | torch.dtype | dict | None,
    checkpoint_files: list[str] | None,
    config: PreTrainedConfig,
    sharded_metadata: dict | None,
    state_dict: dict | None,
    weights_only: bool,
    hf_quantizer: HfQuantizer | None = None,
) -> tuple[PreTrainedConfig, torch.dtype]:
    """Find the correct `dtype` to use based on provided arguments. Also update the `config` based on the
    inferred dtype. We do the following:
    1. If dtype is "auto", we try to read the config, else auto-detect dtype from the loaded state_dict, by checking
    its first weights entry that is of a floating type - we assume all floating dtype weights are of the same dtype
    2. Else, use the dtype provided as a dict or str
    """
    is_sharded = sharded_metadata is not None

    if dtype is not None:
        if isinstance(dtype, str):
            if dtype == "auto":
                if hasattr(config, "dtype") and config.dtype is not None:
                    dtype = config.dtype
                    logger.info(f"Will use dtype={dtype} as defined in model's config object")
                else:
                    if is_sharded and "dtype" in sharded_metadata:
                        dtype = sharded_metadata["dtype"]
                    elif state_dict is not None:
                        dtype = get_state_dict_dtype(state_dict)
                    elif checkpoint_files is not None and checkpoint_files[0].endswith(".gguf"):
                        dtype = torch.float32
                    else:
                        state_dict = load_state_dict(
                            checkpoint_files[0], map_location="meta", weights_only=weights_only
                        )
                        dtype = get_state_dict_dtype(state_dict)
                    logger.info(
                        f"Since the `dtype` attribute can't be found in model's config object, "
                        f"will use dtype={dtype} as derived from model's weights"
                    )
            elif hasattr(torch, dtype):
                dtype = getattr(torch, dtype)
            else:
                raise ValueError(
                    "`dtype` provided as a `str` can only be `'auto'`, or a string representation of a valid `torch.dtype`"
                )

            # cast it to a proper `torch.dtype` object
            dtype = getattr(torch, dtype) if isinstance(dtype, str) else dtype
        elif not isinstance(dtype, (dict, torch.dtype)):
            raise ValueError(
                f"`dtype` can be one of: `torch.dtype`, `'auto'`, a string of a valid `torch.dtype` or a `dict` with valid `dtype` "
                f"for each sub-config in composite configs, but received {dtype}"
            )
    else:
        # set torch.get_default_dtype() (usually fp32) as the default dtype if `None` is provided
        dtype = torch.get_default_dtype()

    if hf_quantizer is not None:
        dtype = hf_quantizer.update_dtype(dtype)

    # Get the main dtype
    if isinstance(dtype, dict):
        main_dtype = dtype.get("", torch.get_default_dtype())
        main_dtype = getattr(torch, main_dtype) if isinstance(main_dtype, str) else main_dtype

        logger.warning_once(
            "Using different dtypes per module is deprecated and will be removed in future versions "
            "Setting different dtypes per backbone model might cause device errors downstream, therefore "
            f"setting the dtype={main_dtype} for all modules."
        )

    else:
        main_dtype = dtype

    # Set it on the config and subconfigs
    config.dtype = main_dtype
    for sub_config_key in config.sub_configs:
        if (sub_config := getattr(config, sub_config_key)) is not None:
            sub_config.dtype = main_dtype

    return config, main_dtype


def _get_dtype(dtype_str: str) -> torch.dtype:
    try:
        dtype = DTYPE_MAP[dtype_str]
    except KeyError:
        dtype = torch.get_default_dtype()

    return dtype


def _get_dtype(dtype):
    """Return np.complex128 for complex dtypes, np.float64 otherwise."""
    if np.issubdtype(dtype, np.complexfloating):
        return np.complex128
    else:
        return np.float64


def _get_dtype(dtype):
    """Return np.complex128 for complex dtypes, np.float64 otherwise."""
    if np.issubdtype(dtype, np.complexfloating):
        return np.complex128
    else:
        return np.float64


def _get_dtype(operators, dtypes=None, xp=None):
    """Returns the promoted dtype from input dtypes and operators."""
    xp = np_compat if xp is None else xp
    if dtypes is None:
        dtypes = []
    for obj in operators:
        if obj is not None and hasattr(obj, "dtype"):
            dtypes.append(obj.dtype)
    return xp_result_type(*dtypes, xp=xp)


def _get_dtype(arr_or_dtype) -> DtypeObj:
    """
    Get the dtype instance associated with an array
    or dtype object.

    Parameters
    ----------
    arr_or_dtype : array-like or dtype
        The array-like or dtype object whose dtype we want to extract.

    Returns
    -------
    obj_dtype : The extract dtype instance from the
                passed in array or dtype object.

    Raises
    ------
    TypeError : The passed in object is None.
    """
    if arr_or_dtype is None:
        raise TypeError("Cannot deduce dtype from null object")

    # fastpath
    if isinstance(arr_or_dtype, np.dtype):
        return arr_or_dtype
    elif isinstance(arr_or_dtype, type):
        return np.dtype(arr_or_dtype)

    # if we have an array-like
    elif hasattr(arr_or_dtype, "dtype"):
        arr_or_dtype = arr_or_dtype.dtype

    return pandas_dtype(arr_or_dtype)

