
def get_differential_var(d):
    text = get_differential_var_str(d.getText())
    return sympy.Symbol(text)

