
def get_constexprs(kernel: JITFunction) -> list[int]:
    return [p.num for p in kernel.params if p.is_constexpr]

