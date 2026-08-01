
def test_noncommutative():
    A, B, C = symbols('A,B,C', commutative=False)

    assert latex(A*B*C**-1) == r"A B C^{-1}"
    assert latex(C**-1*A*B) == r"C^{-1} A B"
    assert latex(A*C**-1*B) == r"A C^{-1} B"


def test_noncommutative():
    A, B, C = symbols('A,B,C', commutative=False)

    assert sstr(A*B*C**-1) == "A*B*C**(-1)"
    assert sstr(C**-1*A*B) == "C**(-1)*A*B"
    assert sstr(A*C**-1*B) == "A*C**(-1)*B"
    assert sstr(sqrt(A)) == "sqrt(A)"
    assert sstr(1/sqrt(A)) == "A**(-1/2)"


def test_noncommutative():
    A, B, C = symbols('A,B,C', commutative=False)

    expr = A*B*C**-1
    ascii_str = \
"""\
     -1\n\
A*B*C  \
"""
    ucode_str = \
"""\
     -1\n\
A⋅B⋅C  \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = C**-1*A*B
    ascii_str = \
"""\
 -1    \n\
C  *A*B\
"""
    ucode_str = \
"""\
 -1    \n\
C  ⋅A⋅B\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = A*C**-1*B
    ascii_str = \
"""\
   -1  \n\
A*C  *B\
"""
    ucode_str = \
"""\
   -1  \n\
A⋅C  ⋅B\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = A*C**-1*B/x
    ascii_str = \
"""\
   -1  \n\
A*C  *B\n\
-------\n\
   x   \
"""
    ucode_str = \
"""\
   -1  \n\
A⋅C  ⋅B\n\
───────\n\
   x   \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str


def test_noncommutative():
    class foo(Expr):
        is_commutative=False
    e = x/(x + x*y)
    c = 1/(1 + y)
    assert apart(e + foo()) == c + foo()


def test_noncommutative():
    class foo(Expr):
        is_commutative=False
    e = x/(x + x*y)
    c = 1/( 1 + y)
    assert cancel(foo(e)) == foo(c)
    assert cancel(e + foo(e)) == c + foo(c)
    assert cancel(e*foo(c)) == c*foo(c)

