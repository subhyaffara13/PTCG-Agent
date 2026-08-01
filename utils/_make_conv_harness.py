
def _make_conv_harness(name,
                       *,
                       lhs_shape=(2, 3, 9, 10),
                       rhs_shape=(3, 3, 4, 5),
                       dtype=np.float32,
                       window_strides=(1, 1),
                       precision=None,
                       padding=((0, 0), (0, 0)),
                       lhs_dilation=(1, 1),
                       rhs_dilation=(1, 1),
                       feature_group_count=1,
                       dimension_numbers=("NCHW", "OIHW", "NCHW"),
                       batch_group_count=1,
                       preferred_element_type=None,
                       works_without_xla=False):
  enable_xla_cases = [True, False] if works_without_xla else [True]

  if (
      preferred_element_type in (np.float64, np.int64, np.complex128)
      and not config.enable_x64.value
  ):
    return

  for enable_xla in enable_xla_cases:
    define(
        lax.conv_general_dilated_p,
        f"{name}_lhs={jtu.format_shape_dtype_string(lhs_shape, dtype)}_rhs={jtu.format_shape_dtype_string(rhs_shape, dtype)}_windowstrides={window_strides}_{padding=!s}_lhsdilation={lhs_dilation}_rhsdilation={rhs_dilation}_dimensionnumbers={dimension_numbers}_featuregroupcount={feature_group_count}_batchgroupcount={batch_group_count}_{precision=}_preferred={jtu.dtype_str(preferred_element_type)}_enablexla={enable_xla}"
        .replace(" ", ""),
        lax.conv_general_dilated,
        [
            RandArg(lhs_shape, dtype),
            RandArg(rhs_shape, dtype),
            StaticArg(window_strides),
            StaticArg(padding),
            StaticArg(lhs_dilation),
            StaticArg(rhs_dilation),
            StaticArg(dimension_numbers),
            StaticArg(feature_group_count),
            StaticArg(batch_group_count),
            StaticArg(precision),
            StaticArg(preferred_element_type),
        ],
        lhs_shape=lhs_shape,
        rhs_shape=rhs_shape,
        dtype=dtype,
        window_strides=window_strides,
        padding=padding,
        lhs_dilation=lhs_dilation,
        rhs_dilation=rhs_dilation,
        dimension_numbers=dimension_numbers,
        feature_group_count=feature_group_count,
        batch_group_count=batch_group_count,
        precision=precision,
        preferred_element_type=preferred_element_type,
        enable_xla=enable_xla,
        jax_unimplemented=[
            # b/183565702 - no integer convolutions for GPU
            Limitation(
                "preferred_element_type not implemented for integers",
                devices="gpu",
                dtypes=(np.int8, np.int16, np.int32, np.int64),
                enabled=(preferred_element_type in [np.int16, np.int32,
                                                    np.int64])),
        ],
    )

