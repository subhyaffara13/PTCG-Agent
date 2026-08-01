
def analyze_var(
    name: str,
    var: Var,
    itype: Instance,
    mx: MemberContext,
    *,
    implicit: bool = False,
    is_trivial_self: bool = False,
) -> Type:
    """Analyze access to an attribute via a Var node.

    This is conceptually part of analyze_member_access and the arguments are similar.
    itype is the instance type in which attribute should be looked up
    original_type is the type of E in the expression E.var
    if implicit is True, the original Var was created as an assignment to self
    if is_trivial_self is True, we can use fast path for bind_self().
    """
    # Found a member variable.
    original_itype = itype
    itype = map_instance_to_supertype(itype, var.info)
    if var.is_settable_property and mx.is_lvalue:
        typ: Type | None = var.setter_type
        if typ is None and var.is_ready:
            # Existing synthetic properties may not set setter type. Fall back to getter.
            typ = var.type
    else:
        typ = var.type
    if typ:
        if isinstance(typ, PartialType):
            return mx.chk.handle_partial_var_type(typ, mx.is_lvalue, var, mx.context)
        if mx.is_lvalue and not mx.suppress_errors:
            if var.is_property and not var.is_settable_property:
                mx.msg.read_only_property(name, itype.type, mx.context)
            if var.is_classvar:
                mx.msg.cant_assign_to_classvar(name, mx.context)
        # This is the most common case for variables, so start with this.
        result = expand_without_binding(typ, var, itype, original_itype, mx)

        # A non-None value indicates that we should actually bind self for this variable.
        call_type: ProperType | None = None
        if var.is_initialized_in_class and (not is_instance_var(var) or mx.is_operator):
            typ = get_proper_type(typ)
            if isinstance(typ, FunctionLike) and not typ.is_type_obj():
                call_type = typ
            elif var.is_property:
                deco_mx = mx.copy_modified(original_type=typ, self_type=typ, is_lvalue=False)
                call_type = get_proper_type(_analyze_member_access("__call__", typ, deco_mx))
            else:
                call_type = typ

        # Bound variables with callable types are treated like methods
        # (these are usually method aliases like __rmul__ = __mul__).
        if isinstance(call_type, FunctionLike) and not call_type.is_type_obj():
            if mx.is_lvalue and not var.is_property and not mx.suppress_errors:
                mx.msg.cant_assign_to_method(mx.context)

        # Bind the self type for each callable component (when needed).
        if call_type and not var.is_staticmethod:
            bound_items = []
            for ct in call_type.items if isinstance(call_type, UnionType) else [call_type]:
                p_ct = get_proper_type(ct)
                if isinstance(p_ct, FunctionLike) and (not p_ct.bound() or var.is_property):
                    item = expand_and_bind_callable(p_ct, var, itype, name, mx, is_trivial_self)
                else:
                    item = expand_without_binding(ct, var, itype, original_itype, mx)
                bound_items.append(item)
            result = UnionType.make_union(bound_items)
    else:
        if not var.is_ready and not mx.no_deferral:
            mx.not_ready_callback(var.name, mx.context)
        # Implicit 'Any' type.
        result = AnyType(TypeOfAny.special_form)
    fullname = f"{var.info.fullname}.{name}"
    hook = mx.chk.plugin.get_attribute_hook(fullname)

    if var.info.is_enum and not mx.is_lvalue:
        if name in var.info.enum_members and name not in {"name", "value"}:
            enum_literal = LiteralType(name, fallback=itype)
            result = itype.copy_modified(last_known_value=enum_literal)
        elif (
            isinstance(p_result := get_proper_type(result), Instance)
            and p_result.type.fullname == "enum.nonmember"
            and p_result.args
        ):
            # Unwrap nonmember similar to class-level access
            result = p_result.args[0]
    if result and not (implicit or var.info.is_protocol and is_instance_var(var)):
        result = analyze_descriptor_access(result, mx)
    if hook:
        result = hook(
            AttributeContext(
                get_proper_type(mx.original_type), result, mx.is_lvalue, mx.context, mx.chk
            )
        )
    return result

