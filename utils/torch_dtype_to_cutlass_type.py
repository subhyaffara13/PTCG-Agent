
def torch_dtype_to_cutlass_type(
    torch_dtype: torch.dtype,
) -> "cutlass_library.library.DataType":  # type: ignore[name-defined] # noqa: F821
    # Import cutlass python scripts.
    assert try_import_cutlass()
    import cutlass_library  # type: ignore[import]

    if torch_dtype == torch.float:
        return cutlass_library.library.DataType.f32
    elif torch_dtype == torch.half:
        return cutlass_library.library.DataType.f16
    elif torch_dtype == torch.bfloat16:
        return cutlass_library.library.DataType.bf16
    elif torch_dtype == torch.float8_e4m3fn:
        return cutlass_library.library.DataType.e4m3
    elif torch_dtype == torch.float8_e5m2:
        return cutlass_library.library.DataType.e5m2
    else:
        raise NotImplementedError(f"Unsupported data type: {torch_dtype=}")

