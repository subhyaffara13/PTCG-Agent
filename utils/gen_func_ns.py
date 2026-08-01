
def gen_func_ns(builder: IRBuilder) -> str:
    """Generate a namespace for a nested function using its outer function names."""
    return "_".join(
        info.name + ("" if not info.class_name else "_" + info.class_name)
        for info in builder.fn_infos
        if info.name and info.name != "<module>"
    )

