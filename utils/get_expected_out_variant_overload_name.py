
def get_expected_out_variant_overload_name(overload_name: str | None) -> str:
    return "out" if not overload_name else f"{overload_name}_out"

