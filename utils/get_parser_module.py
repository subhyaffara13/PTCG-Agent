
def get_parser_module(type_comments: bool = True) -> ParserModule:
    unary_op_classes = _unary_operators_from_module()
    cmp_op_classes = _compare_operators_from_module()
    bool_op_classes = _bool_operators_from_module()
    bin_op_classes = _binary_operators_from_module()
    context_classes = _contexts_from_module()

    return ParserModule(
        unary_op_classes,
        cmp_op_classes,
        bool_op_classes,
        bin_op_classes,
        context_classes,
    )

