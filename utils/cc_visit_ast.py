
def cc_visit_ast(ast_node, **kwargs):
    '''Visit the AST node with :class:`~radon.visitors.ComplexityVisitor`. All
    the keyword arguments are directly passed to the visitor.
    '''
    return ComplexityVisitor.from_ast(ast_node, **kwargs).blocks

