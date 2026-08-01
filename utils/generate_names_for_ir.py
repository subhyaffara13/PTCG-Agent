
def generate_names_for_ir(args: list[Register], blocks: list[BasicBlock]) -> dict[Value, str]:
    """Generate unique names for IR values.

    Give names such as 'r5' to temp values in IR which are useful when
    pretty-printing or generating C. Ensure generated names are unique.
    """
    names: dict[Value, str] = {}
    used_names = set()

    temp_index = 0

    for arg in args:
        names[arg] = arg.name
        used_names.add(arg.name)

    for block in blocks:
        for op in block.ops:
            values = []

            for source in op.sources():
                if source not in names:
                    values.append(source)

            if isinstance(op, (Assign, AssignMulti)):
                values.append(op.dest)
            elif isinstance(op, ControlOp) or op.is_void:
                continue
            elif op not in names:
                values.append(op)

            for value in values:
                if value in names:
                    continue
                if isinstance(value, Register) and value.name:
                    name = value.name
                elif isinstance(value, (Integer, Float, Undef)):
                    continue
                else:
                    name = "r%d" % temp_index
                    temp_index += 1

                # Append _2, _3, ... if needed to make the name unique.
                if name in used_names:
                    n = 2
                    while True:
                        candidate = "%s_%d" % (name, n)
                        if candidate not in used_names:
                            name = candidate
                            break
                        n += 1

                names[value] = name
                used_names.add(name)

    return names

