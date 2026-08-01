
def _del_library(
    captured_impls,
    op_impls,
    captured_defs,
    op_defs,
    registration_handles,
    m,
    schema_to_signature_cache,
):
    for op_def in op_defs:
        name = op_def
        overload_name = ""
        if "." in op_def:
            name, overload_name = op_def.split(".")
        if (
            name,
            overload_name,
        ) in schema_to_signature_cache:
            del schema_to_signature_cache[(name, overload_name)]

    captured_impls -= op_impls
    captured_defs -= op_defs
    for handle in registration_handles:
        handle.destroy()

    if m is not None:
        m.reset()

