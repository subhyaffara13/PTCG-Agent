
def sequence_from_generator_preallocate_helper(
    builder: IRBuilder,
    gen: GeneratorExpr,
    empty_op_llbuilder: Callable[[Value, int], Value],
    set_item_op: Callable[[Value, Value, Value, int], None],
) -> Value | None:
    """Generate a new tuple or list from a simple generator expression.

    Currently we only optimize for simplest generator expression, which means that
    there is no condition list in the generator and only one original sequence with
    one index is allowed.

    e.g.  (1) tuple(f(x) for x in a_list/a_tuple/a_str/a_bytes/an_rtuple)
          (2) list(f(x) for x in a_list/a_tuple/a_str/a_bytes/an_rtuple)
          (3) [f(x) for x in a_list/a_tuple/a_str/a_bytes/an_rtuple]

    Args:
        empty_op_llbuilder: A function that can generate an empty sequence op when
            passed in length. See `new_list_op_with_length` and `new_tuple_op_with_length`
            for detailed implementation.
        set_item_op: A primitive that can modify an arbitrary position of a sequence.
            The op should have three arguments:
                - Self
                - Target position
                - New Value
            See `new_list_set_item_op` and `new_tuple_set_item_op` for detailed
            implementation.
    """
    if len(gen.sequences) == 1 and len(gen.indices) == 1 and len(gen.condlists[0]) == 0:
        line = gen.line
        sequence_expr = gen.sequences[0]
        rtype = builder.node_type(sequence_expr)
        if not (is_sequence_rprimitive(rtype) or isinstance(rtype, (RTuple, RVec))):
            return None

        if isinstance(rtype, RTuple):
            # If input is RTuple, box it to tuple_rprimitive for generic iteration
            # TODO: this can be optimized a bit better with an unrolled ForRTuple helper
            proper_type = get_proper_type(builder.types[sequence_expr])
            assert isinstance(proper_type, TupleType), proper_type

            # the for_loop_helper_with_index crashes for empty tuples, bail out
            if not proper_type.items:
                return None

            proper_types = get_proper_types(proper_type.items)

            get_item_ops: list[LoadLiteral | TupleGet]
            if all(isinstance(typ, LiteralType) for typ in proper_types):
                get_item_ops = [
                    LoadLiteral(cast(LiteralType, typ).value, object_rprimitive)
                    for typ in proper_types
                ]

            else:
                sequence = builder.accept(sequence_expr)
                get_item_ops = [
                    (
                        LoadLiteral(typ.value, object_rprimitive)
                        if isinstance(typ, LiteralType)
                        else TupleGet(sequence, i, line)
                    )
                    for i, typ in enumerate(proper_types)
                ]

            items = list(map(builder.add, get_item_ops))
            sequence = builder.new_tuple(items, line)

        else:
            sequence = builder.accept(sequence_expr)

        length = get_expr_length_value(builder, sequence_expr, sequence, line, use_pyssize_t=True)

        target_op = empty_op_llbuilder(length, line)

        def set_item(item_index: Value) -> None:
            with builder.enter_borrow_scope(line):
                e = builder.accept(gen.left_expr)
            set_item_op(target_op, item_index, e, line)

        for_loop_helper_with_index(
            builder, gen.indices[0], sequence_expr, sequence, set_item, line, length
        )

        return target_op
    return None

