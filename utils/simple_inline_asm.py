
def simple_inline_asm(x):
    if torch.version.hip:
        return inline_asm_elementwise(
            x,
            asm_str="v_mov_b32_e32 $0, $1",
            constraints="=v, v",
            dtype=torch.float32,
        )

    return inline_asm_elementwise(
        x, asm_str="mov.f32 $0, $1;", constraints="=f,f", dtype=torch.float32
    )

