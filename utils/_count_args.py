
def _count_args(proper_kernel_fn_code: str) -> int:
    def_line = proper_kernel_fn_code.splitlines()[0]
    assert def_line.startswith("def ")
    start_idx = def_line.index("(")
    end_idx = def_line.index("):")
    decl_csv = def_line[start_idx + 1 : end_idx]
    comps = decl_csv.split(",")
    return len(comps)

