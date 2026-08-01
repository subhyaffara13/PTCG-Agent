
def build_class_def(ctx, py_def, methods, properties, self_name, assigns):
    r = ctx.make_range(
        py_def.lineno, py_def.col_offset, py_def.col_offset + len("class")
    )
    return ClassDef(
        Ident(r, self_name), [Stmt(method) for method in methods], properties, assigns
    )

