
def read_type(state: State, data: ReadBuffer) -> Type:
    tag = read_tag(data)
    if tag == types.UNBOUND_TYPE:
        name = read_str(data)
        expect_tag(data, LIST_GEN)
        n = read_int_bare(data)
        args = tuple(read_type(state, data) for i in range(n))
        empty_tuple_index = read_bool(data)
        t = read_tag(data)
        if t == LITERAL_NONE:
            original_str_expr = None
        elif t == LITERAL_STR:
            original_str_expr = read_str_bare(data)
        else:
            assert False, f"Unexpected tag for original_str_expr: {t}"
        t = read_tag(data)
        if t == LITERAL_NONE:
            original_str_fallback = None
        elif t == LITERAL_STR:
            original_str_fallback = read_str_bare(data)
        else:
            assert False, f"Unexpected tag for original_str_fallback: {t}"
        unbound = UnboundType(
            name,
            args,
            empty_tuple_index=empty_tuple_index,
            original_str_expr=original_str_expr,
            original_str_fallback=original_str_fallback,
        )
        read_loc(data, unbound)
        expect_end_tag(data)
        return unbound
    elif tag == types.UNION_TYPE:
        expect_tag(data, LIST_GEN)
        n = read_int_bare(data)
        items = [read_type(state, data) for i in range(n)]
        uses_pep604_syntax = read_bool(data)
        t = read_tag(data)
        if t == LITERAL_NONE:
            original_str_expr = None
        elif t == LITERAL_STR:
            original_str_expr = read_str_bare(data)
        else:
            assert False, f"Unexpected tag for original_str_expr: {t}"
        t = read_tag(data)
        if t == LITERAL_NONE:
            original_str_fallback = None
        elif t == LITERAL_STR:
            original_str_fallback = read_str_bare(data)
        else:
            assert False, f"Unexpected tag for original_str_fallback: {t}"
        union = UnionType(items, uses_pep604_syntax=uses_pep604_syntax)
        union.original_str_expr = original_str_expr
        union.original_str_fallback = original_str_fallback
        union.is_evaluated = read_bool(data)
        read_loc(data, union)
        expect_end_tag(data)
        return union
    elif tag == types.LIST_TYPE:
        expect_tag(data, LIST_GEN)
        n = read_int_bare(data)
        items = [read_type(state, data) for i in range(n)]
        type_list = TypeList(items)
        read_loc(data, type_list)
        expect_end_tag(data)
        return type_list
    elif tag == types.TUPLE_TYPE:
        expect_tag(data, LIST_GEN)
        n = read_int_bare(data)
        items = [read_type(state, data) for i in range(n)]
        implicit = read_bool(data)
        tuple_type = TupleType(items, _dummy_fallback, implicit=implicit)
        read_loc(data, tuple_type)
        expect_end_tag(data)
        return tuple_type
    elif tag == types.TYPED_DICT_TYPE:
        expect_tag(data, LIST_GEN)
        n = read_int_bare(data)
        keys = [read_str_opt(data) for i in range(n)]
        expect_tag(data, LIST_GEN)
        n = read_int_bare(data)
        values = [read_type(state, data) for i in range(n)]
        td_items = {}
        extra_items_from = []
        for key, val in zip(keys, values):
            if key is None:
                assert isinstance(val, ProperType)
                extra_items_from.append(val)
            else:
                td_items[key] = val
        typeddict_type = TypedDictType(td_items, set(), set(), _dummy_fallback)
        typeddict_type.extra_items_from = extra_items_from
        read_loc(data, typeddict_type)
        expect_end_tag(data)
        return typeddict_type
    elif tag == types.ELLIPSIS_TYPE:
        ellipsis_type = EllipsisType()
        read_loc(data, ellipsis_type)
        expect_end_tag(data)
        return ellipsis_type
    elif tag == types.RAW_EXPRESSION_TYPE:
        type_name = read_str(data)
        value: types.LiteralValue | str | None
        note: str | None = None
        if type_name == "builtins.bool":
            value = read_bool(data)
        elif type_name == "builtins.int":
            value = read_int(data)
        elif type_name == "builtins.str":
            value = read_str(data)
        elif type_name == "builtins.bytes":
            # Bytes literals are serialized as escaped strings
            value = read_str(data)
        elif type_name == "typing.Any":
            # Invalid type - read None value
            tag = read_tag(data)
            assert tag == LITERAL_NONE, f"Expected LITERAL_NONE for invalid type, got {tag}"
            value = None
            # Read optional note (cache_version >= 2)
            note = read_str_opt(data)
        else:
            assert False, f"Unsupported RawExpressionType: {type_name}"
        raw_type = RawExpressionType(value, type_name, note=note)
        read_loc(data, raw_type)
        expect_end_tag(data)
        return raw_type
    elif tag == types.UNPACK_TYPE:
        inner_type = read_type(state, data)
        from_star_syntax = read_bool(data)
        unpack = UnpackType(inner_type, from_star_syntax=from_star_syntax)
        read_loc(data, unpack)
        if from_star_syntax:
            state.check_min_version("Star unpack syntax", (3, 11), unpack.line, unpack.column)
        expect_end_tag(data)
        return unpack
    elif tag == types.CALL_TYPE:
        return read_call_type(state, data)
    else:
        assert False, tag


def read_type(data: ReadBuffer, tag: Tag | None = None) -> Type:
    if tag is None:
        tag = read_tag(data)
    # The branches here are ordered manually by type "popularity".
    if tag == INSTANCE:
        return Instance.read(data)
    if tag == ANY_TYPE:
        return AnyType.read(data)
    if tag == TYPE_VAR_TYPE:
        return TypeVarType.read(data)
    if tag == CALLABLE_TYPE:
        return CallableType.read(data)
    if tag == NONE_TYPE:
        return NoneType.read(data)
    if tag == UNION_TYPE:
        return UnionType.read(data)
    if tag == LITERAL_TYPE:
        return LiteralType.read(data)
    if tag == TYPE_ALIAS_TYPE:
        return TypeAliasType.read(data)
    if tag == TUPLE_TYPE:
        return TupleType.read(data)
    if tag == TYPED_DICT_TYPE:
        return TypedDictType.read(data)
    if tag == TYPE_TYPE:
        return TypeType.read(data)
    if tag == OVERLOADED:
        return Overloaded.read(data)
    if tag == PARAM_SPEC_TYPE:
        return ParamSpecType.read(data)
    if tag == TYPE_VAR_TUPLE_TYPE:
        return TypeVarTupleType.read(data)
    if tag == UNPACK_TYPE:
        return UnpackType.read(data)
    if tag == PARAMETERS:
        return Parameters.read(data)
    if tag == UNINHABITED_TYPE:
        return UninhabitedType.read(data)
    if tag == UNBOUND_TYPE:
        return UnboundType.read(data)
    if tag == DELETED_TYPE:
        return DeletedType.read(data)
    assert False, f"Unknown type tag {tag}"

