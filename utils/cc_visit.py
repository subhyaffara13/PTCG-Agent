
def cc_visit(code, **kwargs):
    '''Visit the given code with :class:`~radon.visitors.ComplexityVisitor`.
    All the keyword arguments are directly passed to the visitor.
    '''
    return cc_visit_ast(code2ast(code), **kwargs)

