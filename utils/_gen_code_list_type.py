
def _gen_code_list_type(
    arg_name: str, out_name: str, t: ListType, ctype: CType
) -> tuple[list[str], list[str]]:
    in_name = f"{arg_name}_list_in"
    elem_name = f"{arg_name}_elem"
    code = [f"const c10::List<c10::IValue> {in_name} = {arg_name}.toList();"]
    res_name, res_ctype, res_code, decl = argumenttype_ivalue_convert(t.elem, elem_name)
    # handle list type with size, e.g., bool[4]
    if isinstance(t.elem, BaseType) and t.elem.name == BaseTy.bool and t.size:
        code.extend(
            f"""
{ctype.cpp_type(strip_ref=True)} {out_name} = as_array<{res_ctype.cpp_type(strip_ref=True)}, {t.size}>({in_name});
            """.split("\n")
        )
    # we have to use c10::List for optional element. e.g., Tensor?[] -> c10::List<::std::optional<at::Tensor>>
    elif isinstance(t.elem, OptionalType):
        code.extend(
            f"""
{ctype.cpp_type(strip_ref=True)} {out_name};
for (c10::IValue {elem_name}: {in_name}) {{
    {connector.join(res_code)}
    {out_name}.push_back({res_name});
}}
            """.split("\n")
        )
    else:
        # use ArrayRef as default.
        vec_name = arg_name + "_vec"
        # need to bring vector instantiation out of scope so that ArrayRef has valid data
        decl.append(f"std::vector<{res_ctype.cpp_type(strip_ref=True)}> {vec_name};")
        code.extend(
            f"""
for (c10::IValue {elem_name}: {in_name}) {{
    {connector.join(res_code)}
    {vec_name}.push_back({res_name});
}}
{ctype.cpp_type(strip_ref=True)} {out_name}({vec_name});
            """.split("\n")
        )
    return code, decl

