
def test_pretty_print_tensor_expr():
    L = TensorIndexType("L")
    i, j, k = tensor_indices("i j k", L)
    i0 = tensor_indices("i_0", L)
    A, B, C, D = tensor_heads("A B C D", [L])
    H = TensorHead("H", [L, L])

    expr = -i
    ascii_str = \
"""\
-i\
"""
    ucode_str = \
"""\
-i\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = A(i)
    ascii_str = \
"""\
 i\n\
A \n\
  \
"""
    ucode_str = \
"""\
 i\n\
A \n\
  \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = A(i0)
    ascii_str = \
"""\
 i_0\n\
A   \n\
    \
"""
    ucode_str = \
"""\
 i₀\n\
A  \n\
   \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = A(-i)
    ascii_str = \
"""\
  \n\
A \n\
 i\
"""
    ucode_str = \
"""\
  \n\
A \n\
 i\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = -3*A(-i)
    ascii_str = \
"""\
     \n\
-3*A \n\
    i\
"""
    ucode_str = \
"""\
     \n\
-3⋅A \n\
    i\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = H(i, -j)
    ascii_str = \
"""\
 i \n\
H  \n\
  j\
"""
    ucode_str = \
"""\
 i \n\
H  \n\
  j\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = H(i, -i)
    ascii_str = \
"""\
 L_0   \n\
H      \n\
    L_0\
"""
    ucode_str = \
"""\
 L₀  \n\
H    \n\
   L₀\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = H(i, -j)*A(j)*B(k)
    ascii_str = \
"""\
 i     L_0  k\n\
H    *A   *B \n\
  L_0        \
"""
    ucode_str = \
"""\
 i    L₀  k\n\
H   ⋅A  ⋅B \n\
  L₀       \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = (1+x)*A(i)
    ascii_str = \
"""\
         i\n\
(x + 1)*A \n\
          \
"""
    ucode_str = \
"""\
         i\n\
(x + 1)⋅A \n\
          \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = A(i) + 3*B(i)
    ascii_str = \
"""\
   i    i\n\
3*B  + A \n\
         \
"""
    ucode_str = \
"""\
   i    i\n\
3⋅B  + A \n\
         \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

