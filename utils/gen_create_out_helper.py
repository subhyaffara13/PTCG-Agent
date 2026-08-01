
def gen_create_out_helper(backend_index: BackendIndex) -> list[str]:
    if backend_index.dispatch_key == DispatchKey.Meta:
        empty_options = "options.device(at::kMeta)"
    else:
        empty_options = "options"

    empty_impl, empty_strided_impl = gen_empty_impl_names(backend_index)
    if empty_impl is None:
        return []

    return [
        f"""
Tensor create_out(IntArrayRef sizes, IntArrayRef strides, const TensorOptions &options) {{
  if (strides.empty()) {{
      return {empty_impl}(sizes, {empty_options});
  }} else {{
      return {empty_strided_impl}(sizes, strides, {empty_options});
  }}
}}
"""
    ]

