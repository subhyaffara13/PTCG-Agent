
def _is_binary_operator(token_type, text):
    return (
        token_type == tokenize.OP or
        text in {'and', 'or'}
    ) and (
        text not in _SYMBOLIC_OPS
    )

