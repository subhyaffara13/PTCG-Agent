
def validate_super_call(node: FuncBase, mx: MemberContext) -> None:
    unsafe_super = False
    if isinstance(node, FuncDef) and node.is_trivial_body:
        unsafe_super = True
    elif isinstance(node, OverloadedFuncDef):
        if node.impl:
            impl = node.impl if isinstance(node.impl, FuncDef) else node.impl.func
            unsafe_super = impl.is_trivial_body
        elif not node.is_property and node.items:
            assert isinstance(node.items[0], Decorator)
            unsafe_super = node.items[0].func.is_trivial_body
    if unsafe_super:
        mx.msg.unsafe_super(node.name, node.info.name, mx.context)

