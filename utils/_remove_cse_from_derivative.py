
def _remove_cse_from_derivative(replacements, reduced_expressions):
    """
    This function is designed to postprocess the output of a common subexpression
    elimination (CSE) operation. Specifically, it removes any CSE replacement
    symbols from the arguments of ``Derivative`` terms in the expression. This
    is necessary to ensure that the forward Jacobian function correctly handles
    derivative terms.

    Parameters
    ==========

    replacements : list of (Symbol, expression) pairs
        Replacement symbols and relative common subexpressions that have been
        replaced during a CSE operation.

    reduced_expressions : list of SymPy expressions
        The reduced expressions with all the replacements from the
        replacements list above.

    Returns
    =======

    processed_replacements : list of (Symbol, expression) pairs
        Processed replacement list, in the same format of the
        ``replacements`` input list.

    processed_reduced : list of SymPy expressions
        Processed reduced list, in the same format of the
        ``reduced_expressions`` input list.
    """

    def traverse(node, repl_dict):
        if isinstance(node, Derivative):
            return replace_all(node, repl_dict)
        if not node.args:
            return node
        new_args = [traverse(arg, repl_dict) for arg in node.args]
        return node.func(*new_args)

    def replace_all(node, repl_dict):
        result = node
        while True:
            free_symbols = result.free_symbols
            symbols_dict = {k: repl_dict[k] for k in free_symbols if k in repl_dict}
            if not symbols_dict:
                break
            result = result.xreplace(symbols_dict)
        return result

    repl_dict = dict(replacements)
    processed_replacements = [
        (rep_sym, traverse(sub_exp, repl_dict))
        for rep_sym, sub_exp in replacements
    ]
    processed_reduced = [
        red_exp.__class__([traverse(exp, repl_dict) for exp in red_exp])
        for red_exp in reduced_expressions
    ]

    return processed_replacements, processed_reduced

