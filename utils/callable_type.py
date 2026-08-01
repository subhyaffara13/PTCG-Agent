
def callable_type(
    fdef: FuncItem, fallback: Instance, ret_type: Type | None = None
) -> CallableType:
    # TODO: somewhat unfortunate duplication with prepare_method_signature in semanal
    if fdef.info and fdef.has_self_or_cls_argument and fdef.arg_names:
        self_type: Type = fill_typevars(fdef.info)
        if fdef.is_class or fdef.name == "__new__":
            self_type = TypeType.make_normalized(self_type)
        args = [self_type] + [AnyType(TypeOfAny.unannotated)] * (len(fdef.arg_names) - 1)
    else:
        args = [AnyType(TypeOfAny.unannotated)] * len(fdef.arg_names)

    return CallableType(
        args,
        fdef.arg_kinds,
        fdef.arg_names,
        ret_type or AnyType(TypeOfAny.unannotated),
        fallback,
        name=fdef.name,
        line=fdef.line,
        column=fdef.column,
        implicit=True,
        # We need this for better error messages, like missing `self` note:
        definition=fdef if isinstance(fdef, FuncDef) else None,
    )

