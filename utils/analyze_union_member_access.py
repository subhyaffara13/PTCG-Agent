
def analyze_union_member_access(name: str, typ: UnionType, mx: MemberContext) -> Type:
    with mx.msg.disable_type_names():
        results = []
        for subtype in typ.relevant_items():
            # Self types should be bound to every individual item of a union.
            item_mx = mx.copy_modified(self_type=subtype)
            results.append(_analyze_member_access(name, subtype, item_mx))
    return make_simplified_union(results)

