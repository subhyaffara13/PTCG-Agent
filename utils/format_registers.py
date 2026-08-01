
def format_registers(func_ir: FuncIR, names: dict[Value, str]) -> list[str]:
    result = []
    i = 0
    regs = all_values_full(func_ir.arg_regs, func_ir.blocks)
    while i < len(regs):
        i0 = i
        group = [names[regs[i0]]]
        while i + 1 < len(regs) and regs[i + 1].type == regs[i0].type:
            i += 1
            group.append(names[regs[i]])
        i += 1
        result.append("{} :: {}".format(", ".join(group), regs[i0].type))
    return result

