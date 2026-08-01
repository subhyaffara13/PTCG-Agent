
def read_generator_expr(state: State, data: ReadBuffer) -> GeneratorExpr:
    """Helper function to read comprehension data (shared by Generator, ListComp, SetComp)"""
    left_expr = read_expression(state, data)
    n_generators = read_int(data)
    indices = [read_expression(state, data) for _ in range(n_generators)]
    sequences = [read_expression(state, data) for _ in range(n_generators)]
    condlists = [read_expression_list(state, data) for _ in range(n_generators)]
    is_async = [read_bool(data) for _ in range(n_generators)]
    return GeneratorExpr(left_expr, indices, sequences, condlists, is_async)

