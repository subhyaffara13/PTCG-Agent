
def test_boolean_args_order():
    syms = symbols('a:f')

    expr = And(*syms)
    assert latex(expr) == r'a \wedge b \wedge c \wedge d \wedge e \wedge f'

    expr = Or(*syms)
    assert latex(expr) == r'a \vee b \vee c \vee d \vee e \vee f'

    expr = Equivalent(*syms)
    assert latex(expr) == \
        r'a \Leftrightarrow b \Leftrightarrow c \Leftrightarrow d \Leftrightarrow e \Leftrightarrow f'

    expr = Xor(*syms)
    assert latex(expr) == \
        r'a \veebar b \veebar c \veebar d \veebar e \veebar f'

