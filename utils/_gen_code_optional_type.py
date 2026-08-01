
def _gen_code_optional_type(
    arg_name: str, out_name: str, t: OptionalType, ctype: CType
) -> tuple[list[str], list[str]]:
    in_name = f"{arg_name}_opt_in"
    res_name, _, res_code, decl = argumenttype_ivalue_convert(t.elem, in_name)
    return (
        f"""
auto {arg_name}_opt = {arg_name}.toOptional<c10::IValue>();
{ctype.cpp_type(strip_ref=True)} {out_name};
if ({arg_name}_opt.has_value()) {{
    const c10::IValue {in_name} = {arg_name}_opt.value();
    {connector.join(res_code)}
    {out_name} = {ctype.cpp_type(strip_ref=True)}({res_name});
}} else {{
    {out_name} = {ctype.cpp_type(strip_ref=True)}();
}}
        """.split("\n"),
        decl,
    )

