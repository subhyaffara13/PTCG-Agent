
def singledispatch_main_func_name(orig_name: str) -> str:
    return f"__mypyc_singledispatch_main_function_{orig_name}__"

