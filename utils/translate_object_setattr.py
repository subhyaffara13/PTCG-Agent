
def translate_object_setattr(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value | None:
    is_super = isinstance(expr.callee, SuperExpr)
    is_object_callee = is_object(callee)
    if not ((is_super and len(expr.args) >= 2) or (is_object_callee and len(expr.args) >= 3)):
        return None

    self_reg = builder.accept(expr.args[0]) if is_object_callee else builder.self()
    ir = builder.get_current_class_ir()
    if ir and (not ir.is_ext_class or ir.builtin_base or ir.inherits_python):
        return None
    # Need to offset by 1 for super().__setattr__ calls because there is no self arg in this case.
    name_idx = 0 if is_super else 1
    value_idx = 1 if is_super else 2
    attr_name = expr.args[name_idx]
    attr_value = expr.args[value_idx]
    value = builder.accept(attr_value)

    if isinstance(attr_name, StrExpr) and ir and ir.has_attr(attr_name.value):
        name = attr_name.value
        value = builder.coerce(value, ir.attributes[name], expr.line)
        return builder.add(SetAttr(self_reg, name, value, expr.line))

    name_reg = builder.accept(attr_name)
    return builder.call_c(generic_setattr, [self_reg, name_reg, value], expr.line)

