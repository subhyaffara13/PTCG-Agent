
def test_pretty_functions():
    """Tests for Abs, conjugate, exp, function braces, and factorial."""
    expr = (2*x + exp(x))
    ascii_str_1 = \
"""\
       x\n\
2*x + e \
"""
    ascii_str_2 = \
"""\
 x      \n\
e  + 2*x\
"""
    ucode_str_1 = \
"""\
       x\n\
2⋅x + ℯ \
"""
    ucode_str_2 = \
"""\
 x     \n\
ℯ + 2⋅x\
"""
    ucode_str_3 = \
"""\
 x      \n\
ℯ  + 2⋅x\
"""
    assert pretty(expr) in [ascii_str_1, ascii_str_2]
    assert upretty(expr) in [ucode_str_1, ucode_str_2, ucode_str_3]

    expr = Abs(x)
    ascii_str = \
"""\
|x|\
"""
    ucode_str = \
"""\
│x│\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Abs(x/(x**2 + 1))
    ascii_str_1 = \
"""\
|  x   |\n\
|------|\n\
|     2|\n\
|1 + x |\
"""
    ascii_str_2 = \
"""\
|  x   |\n\
|------|\n\
| 2    |\n\
|x  + 1|\
"""
    ucode_str_1 = \
"""\
│  x   │\n\
│──────│\n\
│     2│\n\
│1 + x │\
"""
    ucode_str_2 = \
"""\
│  x   │\n\
│──────│\n\
│ 2    │\n\
│x  + 1│\
"""
    assert pretty(expr) in [ascii_str_1, ascii_str_2]
    assert upretty(expr) in [ucode_str_1, ucode_str_2]

    expr = Abs(1 / (y - Abs(x)))
    ascii_str = \
"""\
    1    \n\
---------\n\
|y - |x||\
"""
    ucode_str = \
"""\
    1    \n\
─────────\n\
│y - │x││\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    n = Symbol('n', integer=True)
    expr = factorial(n)
    ascii_str = \
"""\
n!\
"""
    ucode_str = \
"""\
n!\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = factorial(2*n)
    ascii_str = \
"""\
(2*n)!\
"""
    ucode_str = \
"""\
(2⋅n)!\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = factorial(factorial(factorial(n)))
    ascii_str = \
"""\
((n!)!)!\
"""
    ucode_str = \
"""\
((n!)!)!\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = factorial(n + 1)
    ascii_str_1 = \
"""\
(1 + n)!\
"""
    ascii_str_2 = \
"""\
(n + 1)!\
"""
    ucode_str_1 = \
"""\
(1 + n)!\
"""
    ucode_str_2 = \
"""\
(n + 1)!\
"""

    assert pretty(expr) in [ascii_str_1, ascii_str_2]
    assert upretty(expr) in [ucode_str_1, ucode_str_2]

    expr = subfactorial(n)
    ascii_str = \
"""\
!n\
"""
    ucode_str = \
"""\
!n\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = subfactorial(2*n)
    ascii_str = \
"""\
!(2*n)\
"""
    ucode_str = \
"""\
!(2⋅n)\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    n = Symbol('n', integer=True)
    expr = factorial2(n)
    ascii_str = \
"""\
n!!\
"""
    ucode_str = \
"""\
n!!\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = factorial2(2*n)
    ascii_str = \
"""\
(2*n)!!\
"""
    ucode_str = \
"""\
(2⋅n)!!\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = factorial2(factorial2(factorial2(n)))
    ascii_str = \
"""\
((n!!)!!)!!\
"""
    ucode_str = \
"""\
((n!!)!!)!!\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = factorial2(n + 1)
    ascii_str_1 = \
"""\
(1 + n)!!\
"""
    ascii_str_2 = \
"""\
(n + 1)!!\
"""
    ucode_str_1 = \
"""\
(1 + n)!!\
"""
    ucode_str_2 = \
"""\
(n + 1)!!\
"""

    assert pretty(expr) in [ascii_str_1, ascii_str_2]
    assert upretty(expr) in [ucode_str_1, ucode_str_2]

    expr = 2*binomial(n, k)
    ascii_str = \
"""\
  /n\\\n\
2*| |\n\
  \\k/\
"""
    ucode_str = \
"""\
  ⎛n⎞\n\
2⋅⎜ ⎟\n\
  ⎝k⎠\
"""

    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = 2*binomial(2*n, k)
    ascii_str = \
"""\
  /2*n\\\n\
2*|   |\n\
  \\ k /\
"""
    ucode_str = \
"""\
  ⎛2⋅n⎞\n\
2⋅⎜   ⎟\n\
  ⎝ k ⎠\
"""

    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = 2*binomial(n**2, k)
    ascii_str = \
"""\
  / 2\\\n\
  |n |\n\
2*|  |\n\
  \\k /\
"""
    ucode_str = \
"""\
  ⎛ 2⎞\n\
  ⎜n ⎟\n\
2⋅⎜  ⎟\n\
  ⎝k ⎠\
"""

    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = catalan(n)
    ascii_str = \
"""\
C \n\
 n\
"""
    ucode_str = \
"""\
C \n\
 n\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = catalan(n)
    ascii_str = \
"""\
C \n\
 n\
"""
    ucode_str = \
"""\
C \n\
 n\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = bell(n)
    ascii_str = \
"""\
B \n\
 n\
"""
    ucode_str = \
"""\
B \n\
 n\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = bernoulli(n)
    ascii_str = \
"""\
B \n\
 n\
"""
    ucode_str = \
"""\
B \n\
 n\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = bernoulli(n, x)
    ascii_str = \
"""\
B (x)\n\
 n   \
"""
    ucode_str = \
"""\
B (x)\n\
 n   \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = fibonacci(n)
    ascii_str = \
"""\
F \n\
 n\
"""
    ucode_str = \
"""\
F \n\
 n\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = lucas(n)
    ascii_str = \
"""\
L \n\
 n\
"""
    ucode_str = \
"""\
L \n\
 n\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = tribonacci(n)
    ascii_str = \
"""\
T \n\
 n\
"""
    ucode_str = \
"""\
T \n\
 n\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = stieltjes(n)
    ascii_str = \
"""\
stieltjes \n\
         n\
"""
    ucode_str = \
"""\
γ \n\
 n\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = stieltjes(n, x)
    ascii_str = \
"""\
stieltjes (x)\n\
         n   \
"""
    ucode_str = \
"""\
γ (x)\n\
 n   \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = mathieuc(x, y, z)
    ascii_str = 'C(x, y, z)'
    ucode_str = 'C(x, y, z)'
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = mathieus(x, y, z)
    ascii_str = 'S(x, y, z)'
    ucode_str = 'S(x, y, z)'
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = mathieucprime(x, y, z)
    ascii_str = "C'(x, y, z)"
    ucode_str = "C'(x, y, z)"
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = mathieusprime(x, y, z)
    ascii_str = "S'(x, y, z)"
    ucode_str = "S'(x, y, z)"
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = conjugate(x)
    ascii_str = \
"""\
_\n\
x\
"""
    ucode_str = \
"""\
_\n\
x\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    f = Function('f')
    expr = conjugate(f(x + 1))
    ascii_str_1 = \
"""\
________\n\
f(1 + x)\
"""
    ascii_str_2 = \
"""\
________\n\
f(x + 1)\
"""
    ucode_str_1 = \
"""\
________\n\
f(1 + x)\
"""
    ucode_str_2 = \
"""\
________\n\
f(x + 1)\
"""
    assert pretty(expr) in [ascii_str_1, ascii_str_2]
    assert upretty(expr) in [ucode_str_1, ucode_str_2]

    expr = f(x)
    ascii_str = \
"""\
f(x)\
"""
    ucode_str = \
"""\
f(x)\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = f(x, y)
    ascii_str = \
"""\
f(x, y)\
"""
    ucode_str = \
"""\
f(x, y)\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = f(x/(y + 1), y)
    ascii_str_1 = \
"""\
 /  x     \\\n\
f|-----, y|\n\
 \\1 + y   /\
"""
    ascii_str_2 = \
"""\
 /  x     \\\n\
f|-----, y|\n\
 \\y + 1   /\
"""
    ucode_str_1 = \
"""\
 ⎛  x     ⎞\n\
f⎜─────, y⎟\n\
 ⎝1 + y   ⎠\
"""
    ucode_str_2 = \
"""\
 ⎛  x     ⎞\n\
f⎜─────, y⎟\n\
 ⎝y + 1   ⎠\
"""
    assert pretty(expr) in [ascii_str_1, ascii_str_2]
    assert upretty(expr) in [ucode_str_1, ucode_str_2]

    expr = f(x**x**x**x**x**x)
    ascii_str = \
"""\
 / / / / / x\\\\\\\\\\
 | | | | \\x /||||
 | | | \\x    /|||
 | | \\x       /||
 | \\x          /|
f\\x             /\
"""
    ucode_str = \
"""\
 ⎛ ⎛ ⎛ ⎛ ⎛ x⎞⎞⎞⎞⎞
 ⎜ ⎜ ⎜ ⎜ ⎝x ⎠⎟⎟⎟⎟
 ⎜ ⎜ ⎜ ⎝x    ⎠⎟⎟⎟
 ⎜ ⎜ ⎝x       ⎠⎟⎟
 ⎜ ⎝x          ⎠⎟
f⎝x             ⎠\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = sin(x)**2
    ascii_str = \
"""\
   2   \n\
sin (x)\
"""
    ucode_str = \
"""\
   2   \n\
sin (x)\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = conjugate(a + b*I)
    ascii_str = \
"""\
_     _\n\
a - I*b\
"""
    ucode_str = \
"""\
_     _\n\
a - ⅈ⋅b\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = conjugate(exp(a + b*I))
    ascii_str = \
"""\
 _     _\n\
 a - I*b\n\
e       \
"""
    ucode_str = \
"""\
 _     _\n\
 a - ⅈ⋅b\n\
ℯ       \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = conjugate( f(1 + conjugate(f(x))) )
    ascii_str_1 = \
"""\
___________\n\
 /    ____\\\n\
f\\1 + f(x)/\
"""
    ascii_str_2 = \
"""\
___________\n\
 /____    \\\n\
f\\f(x) + 1/\
"""
    ucode_str_1 = \
"""\
___________\n\
 ⎛    ____⎞\n\
f⎝1 + f(x)⎠\
"""
    ucode_str_2 = \
"""\
___________\n\
 ⎛____    ⎞\n\
f⎝f(x) + 1⎠\
"""
    assert pretty(expr) in [ascii_str_1, ascii_str_2]
    assert upretty(expr) in [ucode_str_1, ucode_str_2]

    expr = f(x/(y + 1), y)
    ascii_str_1 = \
"""\
 /  x     \\\n\
f|-----, y|\n\
 \\1 + y   /\
"""
    ascii_str_2 = \
"""\
 /  x     \\\n\
f|-----, y|\n\
 \\y + 1   /\
"""
    ucode_str_1 = \
"""\
 ⎛  x     ⎞\n\
f⎜─────, y⎟\n\
 ⎝1 + y   ⎠\
"""
    ucode_str_2 = \
"""\
 ⎛  x     ⎞\n\
f⎜─────, y⎟\n\
 ⎝y + 1   ⎠\
"""
    assert pretty(expr) in [ascii_str_1, ascii_str_2]
    assert upretty(expr) in [ucode_str_1, ucode_str_2]

    expr = floor(1 / (y - floor(x)))
    ascii_str = \
"""\
     /     1      \\\n\
floor|------------|\n\
     \\y - floor(x)/\
"""
    ucode_str = \
"""\
⎢   1   ⎥\n\
⎢───────⎥\n\
⎣y - ⌊x⌋⎦\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = ceiling(1 / (y - ceiling(x)))
    ascii_str = \
"""\
       /      1       \\\n\
ceiling|--------------|\n\
       \\y - ceiling(x)/\
"""
    ucode_str = \
"""\
⎡   1   ⎤\n\
⎢───────⎥\n\
⎢y - ⌈x⌉⎥\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = euler(n)
    ascii_str = \
"""\
E \n\
 n\
"""
    ucode_str = \
"""\
E \n\
 n\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = euler(1/(1 + 1/(1 + 1/n)))
    ascii_str = \
"""\
E         \n\
     1    \n\
 ---------\n\
       1  \n\
 1 + -----\n\
         1\n\
     1 + -\n\
         n\
"""

    ucode_str = \
"""\
E         \n\
     1    \n\
 ─────────\n\
       1  \n\
 1 + ─────\n\
         1\n\
     1 + ─\n\
         n\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = euler(n, x)
    ascii_str = \
"""\
E (x)\n\
 n   \
"""
    ucode_str = \
"""\
E (x)\n\
 n   \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = euler(n, x/2)
    ascii_str = \
"""\
  /x\\\n\
E |-|\n\
 n\\2/\
"""
    ucode_str = \
"""\
  ⎛x⎞\n\
E ⎜─⎟\n\
 n⎝2⎠\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

