
def apply_class_attr_hook(
    mx: MemberContext, hook: Callable[[AttributeContext], Type] | None, result: Type
) -> Type | None:
    if hook:
        result = hook(
            AttributeContext(
                get_proper_type(mx.original_type), result, mx.is_lvalue, mx.context, mx.chk
            )
        )
    return result

