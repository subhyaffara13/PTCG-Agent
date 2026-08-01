
def gen_structured(g: NativeFunctionsGroup, backend_index: BackendIndex) -> list[str]:
    meta_name = meta.name(g)
    out_args = structured.impl_arguments(g)
    metadata = backend_index.get_kernel(g)
    if metadata is None:
        return []
    prefix = torch_api_key_word_prefix(backend_index)
    return [
        f"""\
struct {prefix}structured_{metadata.kernel} : public at::meta::structured_{meta_name} {{
void impl({", ".join(a.decl() for a in out_args)});
}};
"""
    ]

