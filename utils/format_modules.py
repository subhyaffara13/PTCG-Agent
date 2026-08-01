
def format_modules(modules: ModuleIRs) -> list[str]:
    ops = []
    for module in modules.values():
        for fn in module.functions:
            ops.extend(format_func(fn))
            ops.append("")
    return ops

