
def h_visit(code):
    '''Compile the code into an AST tree and then pass it to
    :func:`~radon.metrics.h_visit_ast`.
    '''
    return h_visit_ast(ast.parse(code))

