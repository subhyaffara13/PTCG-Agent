
def test_issue_6134():
    from sympy.abc import lamda, t
    phi = Function('phi')

    e = lamda*x*Integral(phi(t)*pi*sin(pi*t), (t, 0, 1)) + lamda*x**2*Integral(phi(t)*2*pi*sin(2*pi*t), (t, 0, 1))
    ucode_str = \
"""\
     1                              1                   \n\
   2 ⌠                              ⌠                   \n\
λ⋅x ⋅⎮ 2⋅π⋅φ(t)⋅sin(2⋅π⋅t) dt + λ⋅x⋅⎮ π⋅φ(t)⋅sin(π⋅t) dt\n\
     ⌡                              ⌡                   \n\
     0                              0                   \
"""
    assert upretty(e) == ucode_str

