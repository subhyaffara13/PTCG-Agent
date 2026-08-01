
def is_torch_flex_attn_available() -> bool:
    return is_torch_available() and version.parse(get_torch_version()) >= version.parse("2.5.0")

