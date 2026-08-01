
def format_func(fn: FuncIR, errors: Sequence[tuple[ErrorSource, str]] = ()) -> list[str]:
    lines = []
    cls_prefix = fn.class_name + "." if fn.class_name else ""
    lines.append(
        "def {}{}({}):".format(cls_prefix, fn.name, ", ".join(arg.name for arg in fn.args))
    )
    names = generate_names_for_ir(fn.arg_regs, fn.blocks)
    for line in format_registers(fn, names):
        lines.append("    " + line)

    source_to_error = defaultdict(list)
    for source, error in errors:
        source_to_error[source].append(error)

    code = format_blocks(fn.blocks, names, source_to_error)
    lines.extend(code)
    return lines

