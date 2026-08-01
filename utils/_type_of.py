
def _type_of(key: torch.dtype | None) -> str:
    # Use the function here to get rid of dependencies on the Triton during the codegen.
    # Refer to Triton implementation here:
    # https://github.com/triton-lang/triton/blob/98b5945d2aef679e00ebca8e07c35c3658ec76de/python/triton/runtime/jit.py#L238
    # `None` is nullptr.  Implicitly convert to *i8.
    if key is None:
        return "*i8"
    dtype_str = str(key).split(".")[-1]
    tys = {
        "bool": "i1",
        "float8e4nv": "fp8e4nv",
        "float8e5": "fp8e5",
        "float8e4b15": "fp8e4b15",
        "float8e4b15x4": "fp8e4b15x4",
        "float8_e4m3fn": "fp8e4nv",
        "float8_e5m2": "fp8e5",
        "float8_e4m3fnuz": "fp8e4b8",
        "float8_e5m2fnuz": "fp8e5b16",
        # TODO: remove when support is added in triton
        # https://github.com/triton-lang/triton/issues/6054
        "float8_e8m0fnu": "u8",
        "float4_e2m1fn_x2": "u8",
        "float16": "fp16",
        "bfloat16": "bf16",
        "float32": "fp32",
        "float64": "fp64",
        "int8": "i8",
        "int16": "i16",
        "int32": "i32",
        "int64": "i64",
        "uint8": "u8",
        "uint16": "u16",
        "uint32": "u32",
        "uint64": "u64",
    }
    # reinterpret can create triton type
    tys.update({v: v for v in list(tys.values())})
    return key if isinstance(key, str) else f"*{tys[dtype_str]}"

