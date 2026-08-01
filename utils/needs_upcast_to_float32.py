
def needs_upcast_to_float32(arg: Any) -> bool:
    return (
        not config.triton.codegen_upcast_to_fp32
        and isinstance(arg, CSEVariable)
        and arg.dtype in (torch.float16, torch.bfloat16)
    )

