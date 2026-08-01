
def h_visit_ast(ast_node):
    '''
    Visit the AST node using the :class:`~radon.visitors.HalsteadVisitor`
    visitor. The results are `HalsteadReport` namedtuples with the following
    fields:

        * h1: the number of distinct operators
        * h2: the number of distinct operands
        * N1: the total number of operators
        * N2: the total number of operands
        * h: the vocabulary, i.e. h1 + h2
        * N: the length, i.e. N1 + N2
        * calculated_length: h1 * log2(h1) + h2 * log2(h2)
        * volume: V = N * log2(h)
        * difficulty: D = h1 / 2 * N2 / h2
        * effort: E = D * V
        * time: T = E / 18 seconds
        * bugs: B = V / 3000 - an estimate of the errors in the implementation

    The actual return of this function is a namedtuple with the following
    fields:

        * total: a `HalsteadReport` namedtuple for the entire scanned file
        * functions: a list of `HalsteadReport`s for each toplevel function

    Nested functions are not tracked.
    '''
    visitor = HalsteadVisitor.from_ast(ast_node)
    total = halstead_visitor_report(visitor)
    functions = [
        (v.context, halstead_visitor_report(v))
        for v in visitor.function_visitors
    ]

    return Halstead(total, functions)

