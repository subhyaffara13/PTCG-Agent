
def build_expression_eager(_, expr):
    """Build a eager tensorflow function based on ``arrays`` and ``expr``."""

    def tensorflow_eager_contract(*arrays):
        return expr._contract([to_tensorflow(x) for x in arrays], backend="tensorflow").numpy()

    return tensorflow_eager_contract

