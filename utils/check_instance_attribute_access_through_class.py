
def check_instance_attribute_access_through_class(
    builder: IRBuilder, expr: MemberExpr, typ: ProperType | None
) -> None:
    """Report error if accessing an instance attribute through class object."""
    if isinstance(expr.expr, RefExpr):
        node = expr.expr.node
        if isinstance(typ, TypeType) and isinstance(typ.item, Instance):
            # TODO: Handle other item types
            node = typ.item.type
        if isinstance(node, TypeInfo):
            class_ir = builder.mapper.type_to_ir.get(node)
            if class_ir is not None and class_ir.is_ext_class:
                sym = node.get(expr.name)
                if (
                    sym is not None
                    and isinstance(sym.node, Var)
                    and not sym.node.is_classvar
                    and not sym.node.is_final
                ):
                    builder.error(
                        'Cannot access instance attribute "{}" through class object'.format(
                            expr.name
                        ),
                        expr.line,
                    )
                    builder.note(
                        '(Hint: Use "x: Final = ..." or "x: ClassVar = ..." to define '
                        "a class attribute)",
                        expr.line,
                    )

