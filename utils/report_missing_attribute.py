
def report_missing_attribute(
    original_type: Type,
    typ: Type,
    name: str,
    mx: MemberContext,
    override_info: TypeInfo | None = None,
) -> Type:
    if mx.suppress_errors:
        return AnyType(TypeOfAny.from_error)
    error_code = mx.msg.has_no_attr(original_type, typ, name, mx.context, mx.module_symbol_table)
    if not mx.msg.prefer_simple_messages():
        if may_be_awaitable_attribute(name, typ, mx, override_info):
            mx.msg.possible_missing_await(mx.context, error_code)
    return AnyType(TypeOfAny.from_error)

