
def generate_non_out_variant_call(
    g: NativeFunctionsGroup, backend_index: BackendIndex
) -> str:
    schema = g.functional.func
    if schema.is_out_fn():
        raise AssertionError(f"Expected non-out function, got {schema}")
    kernel_name = get_kernel_name(g, backend_index)
    arg_names = (arg.name for arg in schema.schema_order_arguments())
    namespace_name = "cpu" if g.structured else "native"
    return f"at::{namespace_name}::{kernel_name}({','.join(arg_names)})"

