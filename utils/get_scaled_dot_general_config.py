
def get_scaled_dot_general_config(mode: Literal['nvfp4', 'mxfp8'],
                                  global_scale: Array | None = None):
    r"""Get quantization configs for scaled_dot_general.

    Create quantization configs for the `jax.nn.scaled_dot_general`.

    See Also:
      - :func:`jax.nn.scaled_dot_general`: Scaled dot general function.
    """

    if mode == 'nvfp4':
        one = jnp.ones((1,), dtype=np.float32)
        return BlockScaleConfig(
            mode='nvfp4',
            block_size=16,
            data_type=dtypes.float4_e2m1fn,
            scale_type=dtypes.float8_e4m3fn,
            global_scale=one if global_scale is None else global_scale,
            infer_only=False
        )
    elif mode == 'mxfp8':
        return BlockScaleConfig(
            mode='mxfp8',
            block_size=32,
            data_type=dtypes.float8_e4m3fn,
            scale_type=dtypes.float8_e8m0fnu,
            global_scale=None,
            infer_only=False
        )
    else:
        raise ValueError(f"Unsupported mode: {mode}")

