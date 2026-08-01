
def check_unsupported_cls_assignment(builder: IRBuilder, stmt: AssignmentStmt) -> None:
    fn = builder.fn_info
    method_args = fn.fitem.arg_names
    if fn.name != "__new__" or len(method_args) == 0:
        return

    ir = builder.get_current_class_ir()
    if ir is None or ir.inherits_python or not ir.is_ext_class:
        return

    cls_arg = method_args[0]

    def flatten(lvalues: list[Expression]) -> list[Expression]:
        flat = []
        for lvalue in lvalues:
            if isinstance(lvalue, (TupleExpr, ListExpr)):
                flat += flatten(lvalue.items)
            else:
                flat.append(lvalue)
        return flat

    lvalues = flatten(stmt.lvalues)

    for lvalue in lvalues:
        if isinstance(lvalue, NameExpr) and lvalue.name == cls_arg:
            # Disallowed because it could break the transformation of object.__new__ calls
            # inside __new__ methods.
            builder.error(
                f'Assignment to argument "{cls_arg}" in "__new__" method unsupported', stmt.line
            )

