
def reduction_prefix_array(
    acc_var: str | CSEVariable,
    acc_type: str,
    reduction_type: str,
    dtype: torch.dtype,
    len: str | int,
    init_fn,
):
    """
    MSVC don't support dynamic array(VLA). So we use std::unique_ptr here.
    Ref: https://stackoverflow.com/questions/56555406/creating-dynamic-sized-array-using-msvc-c-compiler
    MSVC is the only one compiler without VLA. support. Since MSVC can't get good performance here.
    We just use unique_ptr make it works on MSVC.
    For other compilers, we continue to use VLA to get best performance.
    """
    code_buffer = IndentedBuffer()
    acc_decl = (
        f"auto {acc_var}_arr = std::make_unique<{acc_type}[]>({len});"
        if cpp_builder.is_msvc_cl()
        else f"{acc_type} {acc_var}_arr[{len}];"
    )
    code_buffer.writeline(f"{acc_decl}")
    code_buffer.writelines(
        [
            f"for (int i = 0; i < {len}; i++)",
            "{",
            f"    {acc_var}_arr[i] = {init_fn(reduction_type, dtype)};",
            "}",
        ],
    )
    return code_buffer

