
def function_annotations(func_ir: FuncIR, tree: MypyFile) -> dict[int, list[Annotation]]:
    """Generate annotations based on mypyc IR."""
    # TODO: check if func_ir.line is -1
    anns: dict[int, list[Annotation]] = {}
    for block in func_ir.blocks:
        for op in block.ops:
            if isinstance(op, CallC):
                name = op.function_name
                ann: str | Annotation | None = None
                if name == "CPyObject_GetAttr":
                    attr_name = get_str_literal(op.args[1])
                    if attr_name in ("__prepare__", "GeneratorExit", "StopIteration"):
                        # These attributes are internal to mypyc/CPython, and/or accessed
                        # implicitly in generated code. The user has little control over
                        # them.
                        ann = None
                    elif attr_name:
                        ann = f'Get non-native attribute "{attr_name}".'
                    else:
                        ann = "Dynamic attribute lookup."
                elif name == "PyObject_SetAttr":
                    attr_name = get_str_literal(op.args[1])
                    if attr_name == "__mypyc_attrs__":
                        # This is set implicitly and can't be avoided.
                        ann = None
                    elif attr_name:
                        ann = f'Set non-native attribute "{attr_name}".'
                    else:
                        ann = "Dynamic attribute set."
                elif name == "PyObject_VectorcallMethod":
                    method_name = get_str_literal(op.args[0])
                    if method_name:
                        ann = f'Call non-native method "{method_name}" (it may be defined in a non-native class, or decorated).'
                    else:
                        ann = "Dynamic method call."
                elif name in op_hints:
                    ann = op_hints[name]
                elif name in ("CPyDict_GetItem", "CPyDict_SetItem"):
                    if (
                        isinstance(op.args[0], LoadStatic)
                        and isinstance(op.args[1], LoadLiteral)
                        and func_ir.name != "__top_level__"
                    ):
                        load = op.args[0]
                        name = str(op.args[1].value)
                        sym = tree.names.get(name)
                        if (
                            sym
                            and sym.node
                            and load.namespace == "static"
                            and load.identifier == "globals"
                        ):
                            if sym.node.fullname in stdlib_hints:
                                ann = stdlib_hints[sym.node.fullname]
                            elif isinstance(sym.node, Var):
                                ann = (
                                    f'Access global "{name}" through namespace '
                                    + "dictionary (hint: access is faster if you can make it Final)."
                                )
                            else:
                                ann = f'Access "{name}" through global namespace dictionary.'
                if ann:
                    if isinstance(ann, str):
                        ann = Annotation(ann)
                    anns.setdefault(op.line, []).append(ann)
    return anns

