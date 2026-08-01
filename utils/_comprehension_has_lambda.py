
def _comprehension_has_lambda(node: GeneratorExpr | DictionaryComprehension) -> bool:
    """Return True if a comprehension body contains a lambda.

    Only checks body expressions (left_expr/key/value and conditions),
    not the sequences, since sequences are evaluated in the enclosing scope.
    """
    checker = _LambdaChecker()
    if isinstance(node, GeneratorExpr):
        node.left_expr.accept(checker)
    else:
        node.key.accept(checker)
        node.value.accept(checker)
    for conds in node.condlists:
        for cond in conds:
            cond.accept(checker)
    return checker.found

