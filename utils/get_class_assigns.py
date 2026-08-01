
def get_class_assigns(ctx, cls_ast):
    assigns = []

    def maybe_build_assign(builder, entry) -> None:
        nonlocal assigns
        try:
            assigns.append(builder(ctx, entry))
        except NotSupportedError:
            pass

    for entry in cls_ast.body:
        if isinstance(entry, ast.Assign):
            maybe_build_assign(StmtBuilder.build_Assign, entry)
        elif isinstance(entry, ast.AnnAssign):
            maybe_build_assign(StmtBuilder.build_AnnAssign, entry)
    return assigns

