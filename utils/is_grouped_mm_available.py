
def is_grouped_mm_available() -> bool:
    return is_torch_available() and version.parse(get_torch_version()) >= version.parse("2.9.0")

