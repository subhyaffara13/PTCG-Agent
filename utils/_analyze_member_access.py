
def _analyze_member_access(
    name: str, typ: Type, mx: MemberContext, override_info: TypeInfo | None = None
) -> Type:
    typ = get_proper_type(typ)
    if isinstance(typ, Instance):
        return analyze_instance_member_access(name, typ, mx, override_info)
    elif isinstance(typ, AnyType):
        # The base object has dynamic type.
        return AnyType(TypeOfAny.from_another_any, source_any=typ)
    elif isinstance(typ, UnionType):
        return analyze_union_member_access(name, typ, mx)
    elif isinstance(typ, FunctionLike) and typ.is_type_obj():
        return analyze_type_callable_member_access(name, typ, mx)
    elif isinstance(typ, TypeType):
        return analyze_type_type_member_access(name, typ, mx, override_info)
    elif isinstance(typ, TupleType):
        # Actually look up from the fallback instance type.
        return _analyze_member_access(name, tuple_fallback(typ), mx, override_info)
    elif isinstance(typ, (LiteralType, FunctionLike)):
        # Actually look up from the fallback instance type.
        return _analyze_member_access(name, typ.fallback, mx, override_info)
    elif isinstance(typ, TypedDictType):
        return analyze_typeddict_access(name, typ, mx, override_info)
    elif isinstance(typ, NoneType):
        return analyze_none_member_access(name, typ, mx)
    elif isinstance(typ, TypeVarLikeType):
        if isinstance(typ, TypeVarType) and typ.values:
            return _analyze_member_access(
                name, make_simplified_union(typ.values), mx, override_info
            )
        return _analyze_member_access(name, typ.upper_bound, mx, override_info)
    elif isinstance(typ, DeletedType):
        if not mx.suppress_errors:
            mx.msg.deleted_as_rvalue(typ, mx.context)
        return AnyType(TypeOfAny.from_error)
    elif isinstance(typ, UninhabitedType):
        attr_type = UninhabitedType()
        attr_type.ambiguous = typ.ambiguous
        return attr_type
    return report_missing_attribute(mx.original_type, typ, name, mx)

