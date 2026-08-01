
def is_flash_attn_available():
    return (
        is_flash_attn_4_available()
        or is_flash_attn_3_available()
        or is_flash_attn_2_available()
        or is_torch_npu_available()
        or is_torch_xpu_available()
    )

