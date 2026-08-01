
def typed_dict_update_signature_callback(ctx: MethodSigContext) -> CallableType:
    """Try to infer a better signature type for methods that update `TypedDict`.

    This includes: `TypedDict.update`, `TypedDict.__or__`, `TypedDict.__ror__`,
    and `TypedDict.__ior__`.
    """
    signature = ctx.default_signature
    if isinstance(ctx.type, TypedDictType) and len(signature.arg_types) == 1:
        arg_type = get_proper_type(signature.arg_types[0])
        if not isinstance(arg_type, TypedDictType):
            return signature
        arg_type = ctx.type.copy_modified(
            fallback=arg_type.create_anonymous_fallback(), required_keys=set()
        )
        if ctx.args and ctx.args[0]:
            if signature.name in _TP_DICT_MUTATING_METHODS:
                # If we want to mutate this object in place, we need to set this flag,
                # it will trigger an extra check in TypedDict's checker.
                arg_type.to_be_mutated = True
            with ctx.api.msg.filter_errors(
                filter_errors=lambda name, info: info.code != codes.TYPEDDICT_READONLY_MUTATED,
                save_filtered_errors=True,
            ):
                inferred = get_proper_type(
                    ctx.api.get_expression_type(ctx.args[0][0], type_context=arg_type)
                )
            if arg_type.to_be_mutated:
                arg_type.to_be_mutated = False  # Done!
            possible_tds = []
            if isinstance(inferred, TypedDictType):
                possible_tds = [inferred]
            elif isinstance(inferred, UnionType):
                possible_tds = [
                    t
                    for t in get_proper_types(inferred.relevant_items())
                    if isinstance(t, TypedDictType)
                ]
            items = []
            for td in possible_tds:
                item = arg_type.copy_modified(
                    required_keys=(arg_type.required_keys | td.required_keys)
                    & arg_type.items.keys()
                )
                if not ctx.api.options.extra_checks:
                    item = item.copy_modified(item_names=list(td.items))
                items.append(item)
            if items:
                arg_type = make_simplified_union(items)
        return signature.copy_modified(arg_types=[arg_type])
    return signature

