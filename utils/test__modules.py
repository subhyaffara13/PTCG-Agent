
def test_Modules():
    from sympy.polys.domains import QQ
    from sympy.polys.agca import homomorphism

    R = QQ.old_poly_ring(x, y)
    F = R.free_module(2)
    M = F.submodule([x, y], [1, x**2])

    assert latex(F) == r"{\mathbb{Q}\left[x, y\right]}^{2}"
    assert latex(M) == \
        r"\left\langle {\left[ {x},{y} \right]},{\left[ {1},{x^{2}} \right]} \right\rangle"

    I = R.ideal(x**2, y)
    assert latex(I) == r"\left\langle {x^{2}},{y} \right\rangle"

    Q = F / M
    assert latex(Q) == \
        r"\frac{{\mathbb{Q}\left[x, y\right]}^{2}}{\left\langle {\left[ {x},"\
        r"{y} \right]},{\left[ {1},{x^{2}} \right]} \right\rangle}"
    assert latex(Q.submodule([1, x**3/2], [2, y])) == \
        r"\left\langle {{\left[ {1},{\frac{x^{3}}{2}} \right]} + {\left"\
        r"\langle {\left[ {x},{y} \right]},{\left[ {1},{x^{2}} \right]} "\
        r"\right\rangle}},{{\left[ {2},{y} \right]} + {\left\langle {\left[ "\
        r"{x},{y} \right]},{\left[ {1},{x^{2}} \right]} \right\rangle}} \right\rangle"

    h = homomorphism(QQ.old_poly_ring(x).free_module(2),
                     QQ.old_poly_ring(x).free_module(2), [0, 0])

    assert latex(h) == \
        r"{\left[\begin{matrix}0 & 0\\0 & 0\end{matrix}\right]} : "\
        r"{{\mathbb{Q}\left[x\right]}^{2}} \to {{\mathbb{Q}\left[x\right]}^{2}}"

