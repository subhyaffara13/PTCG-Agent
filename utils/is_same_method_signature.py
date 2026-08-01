
def is_same_method_signature(a: FuncSignature, b: FuncSignature) -> bool:
    return (
        len(a.args) == len(b.args)
        and is_same_type(a.ret_type, b.ret_type)
        and all(
            is_same_type(t1.type, t2.type)
            and ((t1.pos_only and t2.pos_only) or t1.name == t2.name)
            and t1.optional == t2.optional
            for t1, t2 in zip(a.args[1:], b.args[1:])
        )
    )

