
def zero_symbols(expression):
    return S.Zero if isinstance(expression, Symbol) else expression

