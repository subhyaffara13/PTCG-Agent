
def test_pretty_print_tensor_partial_deriv():
    from sympy.tensor.toperators import PartialDerivative

    L = TensorIndexType("L")
    i, j, k = tensor_indices("i j k", L)

    A, B, C, D = tensor_heads("A B C D", [L])

    H = TensorHead("H", [L, L])

    expr = PartialDerivative(A(i), A(j))
    ascii_str = \
"""\
 d / i\\\n\
---|A |\n\
  j\\  /\n\
dA     \n\
       \
"""
    ucode_str = \
"""\
 ∂ ⎛ i⎞\n\
───⎜A ⎟\n\
  j⎝  ⎠\n\
∂A     \n\
       \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = A(i)*PartialDerivative(H(k, -i), A(j))
    ascii_str = \
"""\
 L_0  d / k   \\\n\
A   *---|H    |\n\
       j\\  L_0/\n\
     dA        \n\
               \
"""
    ucode_str = \
"""\
 L₀  ∂ ⎛ k  ⎞\n\
A  ⋅───⎜H   ⎟\n\
      j⎝  L₀⎠\n\
    ∂A       \n\
             \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = A(i)*PartialDerivative(B(k)*C(-i) + 3*H(k, -i), A(j))
    ascii_str = \
"""\
 L_0  d /   k       k     \\\n\
A   *---|3*H     + B *C   |\n\
       j\\    L_0       L_0/\n\
     dA                    \n\
                           \
"""
    ucode_str = \
"""\
 L₀  ∂ ⎛   k      k    ⎞\n\
A  ⋅───⎜3⋅H    + B ⋅C  ⎟\n\
      j⎝    L₀       L₀⎠\n\
    ∂A                  \n\
                        \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = (A(i) + B(i))*PartialDerivative(C(j), D(j))
    ascii_str = \
"""\
/ i    i\\   d  / L_0\\\n\
|A  + B |*-----|C   |\n\
\\       /   L_0\\    /\n\
          dD         \n\
                     \
"""
    ucode_str = \
"""\
⎛ i    i⎞  ∂  ⎛ L₀⎞\n\
⎜A  + B ⎟⋅────⎜C  ⎟\n\
⎝       ⎠   L₀⎝   ⎠\n\
          ∂D       \n\
                   \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = (A(i) + B(i))*PartialDerivative(C(-i), D(j))
    ascii_str = \
"""\
/ L_0    L_0\\  d /    \\\n\
|A    + B   |*---|C   |\n\
\\           /   j\\ L_0/\n\
              dD       \n\
                       \
"""
    ucode_str = \
"""\
⎛ L₀    L₀⎞  ∂ ⎛   ⎞\n\
⎜A   + B  ⎟⋅───⎜C  ⎟\n\
⎝         ⎠   j⎝ L₀⎠\n\
            ∂D      \n\
                    \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = PartialDerivative(B(-i) + A(-i), A(-j), A(-n))
    ucode_str = """\
   2            \n\
  ∂    ⎛       ⎞\n\
───────⎜A  + B ⎟\n\
       ⎝ i    i⎠\n\
∂A  ∂A          \n\
  n   j         \
"""
    assert upretty(expr) == ucode_str

    expr = PartialDerivative(3*A(-i), A(-j), A(-n))
    ucode_str = """\
   2         \n\
  ∂    ⎛    ⎞\n\
───────⎜3⋅A ⎟\n\
       ⎝   i⎠\n\
∂A  ∂A       \n\
  n   j      \
"""
    assert upretty(expr) == ucode_str

    expr = TensorElement(H(i, j), {i:1})
    ascii_str = \
"""\
 i=1,j\n\
H     \n\
      \
"""
    ucode_str = ascii_str
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = TensorElement(H(i, j), {i: 1, j: 1})
    ascii_str = \
"""\
 i=1,j=1\n\
H       \n\
        \
"""
    ucode_str = ascii_str
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = TensorElement(H(i, j), {j: 1})
    ascii_str = \
"""\
 i,j=1\n\
H     \n\
      \
"""
    ucode_str = ascii_str

    expr = TensorElement(H(-i, j), {-i: 1})
    ascii_str = \
"""\
    j\n\
H    \n\
 i=1 \
"""
    ucode_str = ascii_str
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

