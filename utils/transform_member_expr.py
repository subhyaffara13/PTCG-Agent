
def transform_member_expr(builder: IRBuilder, expr: MemberExpr) -> Value:
    # Special Cases
    if expr.fullname in ("typing.TYPE_CHECKING", "typing_extensions.TYPE_CHECKING"):
        return builder.false(expr.line)

    # First check if this is maybe a final class/module attribute.
    final = builder.get_final_ref(expr)
    if final is not None:
        fullname, final_var, native = final
        final_type = builder.types.get(expr) or final_var.type
        if final_type is None:
            final_type = AnyType(TypeOfAny.special_form)
        value = builder.emit_load_final(
            final_var, fullname, final_var.name, native, final_type, expr.line
        )
        if value is not None:
            return value

    math_literal = transform_math_literal(builder, expr.fullname, expr.line)
    if math_literal is not None:
        return math_literal

    if isinstance(expr.node, MypyFile) and expr.node.fullname in builder.imports:
        return builder.load_module(expr.node.fullname)

    rtype = builder.node_type(expr)
    # Borrowing a native attribute read is unsafe on free-threaded builds, since another
    # thread could concurrently reassign the attribute and free the old value. We still borrow
    # in two cases:
    #  - Native Final attributes are read-only at runtime, so they can never be reassigned.
    #  - Vec-typed attributes require manual synchronization, so we borrow them liberally.
    can_borrow = builder.is_native_attr_ref(expr) and (
        not IS_FREE_THREADED or isinstance(rtype, RVec) or builder.is_final_native_attr_ref(expr)
    )
    obj = builder.accept(expr.expr, can_borrow=can_borrow)

    if (
        is_object_rprimitive(obj.type)
        and expr.name == "__name__"
        and builder.options.capi_version >= (3, 11)
    ):
        return builder.primitive_op(name_op, [obj], expr.line)

    if isinstance(obj.type, RInstance) and expr.name == "__class__":
        # A non-native class could override "__class__" using "__getattribute__", so
        # only apply to RInstance types.
        return builder.primitive_op(type_op, [obj], expr.line)

    # Special case: for named tuples transform attribute access to faster index access.
    typ = get_proper_type(builder.types.get(expr.expr))
    if isinstance(typ, TupleType) and typ.partial_fallback.type.is_named_tuple:
        fields = typ.partial_fallback.type.metadata["namedtuple"]["fields"]
        if expr.name in fields:
            index = builder.builder.load_int(fields.index(expr.name))
            return builder.gen_method_call(obj, "__getitem__", [index], rtype, expr.line)

    check_instance_attribute_access_through_class(builder, expr, typ)

    is_final = builder.is_final_native_attr_ref(expr)
    scope = KEEP_ALIVE_SHORT_LIVED
    if (
        is_final
        and builder.expression_depth > 1
        and value_borrow_scope(builder, obj) >= KEEP_ALIVE_WHOLE_EXPRESSION
        # Don't borrow across the whole expression if the borrow root can be
        # rebound via a walrus assignment
        and not builder.root_is_reassigned(obj)
        # Don't borrow across a suspension point (await/yield/yield from), since
        # the borrow would not survive the suspend (registers aren't spilled).
        and not builder.expr_has_suspend
    ):
        scope = KEEP_ALIVE_WHOLE_EXPRESSION
    borrow = (can_borrow and builder.can_borrow) or scope == KEEP_ALIVE_WHOLE_EXPRESSION
    return builder.builder.get_attr(
        obj, expr.name, rtype, expr.line, borrow=borrow, borrow_scope=scope
    )

