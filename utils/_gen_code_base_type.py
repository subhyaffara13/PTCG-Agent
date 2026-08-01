
def _gen_code_base_type(
    arg_name: str, out_name: str, ctype: CType
) -> tuple[list[str], list[str]]:
    return [
        f"{ctype.cpp_type(strip_ref=True)} {out_name} = {arg_name}.to<{ctype.cpp_type(strip_ref=True)}>();"
    ], []

