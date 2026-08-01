
def view_func_name(
    f: NativeFunction, include_namespace: bool = False, camel_case: bool = True
) -> str:
    name = f.func.name.unambiguous_name()
    view_func_name = f"{name.replace('.', '_')}_view_func"
    if camel_case:
        is_private = view_func_name.startswith("_")
        view_func_name = "".join(
            [p.title() for p in view_func_name.replace(".", "_").split("_")]
        )
        if is_private:
            # put the leading underscore back in
            view_func_name = f"_{view_func_name}"
    namespace = "torch::autograd::generated::" if include_namespace else ""
    return f"{namespace}{view_func_name}"

