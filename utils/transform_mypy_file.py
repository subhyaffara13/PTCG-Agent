
def transform_mypy_file(builder: IRBuilder, mypyfile: MypyFile) -> None:
    """Generate IR for a single module."""

    if mypyfile.fullname in ("typing", "abc"):
        # These module are special; their contents are currently all
        # built-in primitives.
        return

    builder.set_module(mypyfile.fullname, mypyfile.path)

    classes = [node for node in mypyfile.defs if isinstance(node, ClassDef)]

    # Collect all classes.
    for cls in classes:
        ir = builder.mapper.type_to_ir[cls.info]
        builder.classes.append(ir)

    builder.enter("<module>")

    # Make sure we have a builtins import
    builder.gen_import("builtins", 1)

    # Generate ops.
    for node in mypyfile.defs:
        builder.accept(node)

    builder.maybe_add_implicit_return()

    # Generate special function representing module top level.
    args, _, blocks, ret_type, _ = builder.leave()
    sig = FuncSignature([], none_rprimitive)
    func_ir = FuncIR(
        FuncDecl(TOP_LEVEL_NAME, None, builder.module_name, sig),
        args,
        blocks,
        traceback_name="<module>",
    )
    builder.functions.append(func_ir)

