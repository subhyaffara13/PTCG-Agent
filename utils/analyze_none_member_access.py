
def analyze_none_member_access(name: str, typ: NoneType, mx: MemberContext) -> Type:
    if name == "__bool__":
        literal_false = LiteralType(False, fallback=mx.named_type("builtins.bool"))
        return CallableType(
            arg_types=[],
            arg_kinds=[],
            arg_names=[],
            ret_type=literal_false,
            fallback=mx.named_type("builtins.function"),
        )
    else:
        return _analyze_member_access(name, mx.named_type("builtins.object"), mx)

