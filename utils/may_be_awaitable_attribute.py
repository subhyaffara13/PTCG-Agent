
def may_be_awaitable_attribute(
    name: str, typ: Type, mx: MemberContext, override_info: TypeInfo | None = None
) -> bool:
    """Check if the given type has the attribute when awaited."""
    if mx.chk.checking_missing_await:
        # Avoid infinite recursion.
        return False
    with mx.chk.checking_await_set(), mx.msg.filter_errors() as local_errors:
        aw_type = mx.chk.get_precise_awaitable_type(typ, local_errors)
        if aw_type is None:
            return False
        _ = _analyze_member_access(
            name, aw_type, mx.copy_modified(self_type=aw_type), override_info
        )
        return not local_errors.has_new_errors()

