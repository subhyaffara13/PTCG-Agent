
def gen_maybe_create_proxy_helper(backend_index: BackendIndex) -> list[str]:
    _, empty_strided_impl = gen_empty_impl_names(backend_index)
    return (
        []
        if empty_strided_impl is None
        else [
            f"""
std::optional<Tensor> maybe_create_proxy(const Tensor &out, IntArrayRef sizes, IntArrayRef strides, const TensorOptions &options) {{
  if (out.strides() != strides) {{
    return {empty_strided_impl}(sizes, strides, options);
  }}
  return std::nullopt;
}}
"""
        ]
    )

