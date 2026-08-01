
def _ensure_fp4_dtype_registered():
    """Patch cutlass_api to handle torch.float4_e2m1fn_x2 -> cutlass.Float4E2M1FN.

    NOTE: cutlass_api doesn't natively map this dtype. We patch the lookup function
    in-place so all callers (including TensorWrapper) pick up the change.
    Remove once cutlass_api adds native FP4 support.
    """
    import cutlass_api.utils

    try:
        cutlass_api.utils.cutlass_type_from_torch_type(torch.float4_e2m1fn_x2)
    except (KeyError, AttributeError):
        import cutlass

        _orig = cutlass_api.utils.cutlass_type_from_torch_type

        def _patched(dtype):
            if dtype == torch.float4_e2m1fn_x2:
                return cutlass.Float4E2M1FN
            return _orig(dtype)

        cutlass_api.utils.cutlass_type_from_torch_type = _patched

