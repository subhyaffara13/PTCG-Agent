
def test_latex_diffgeom():
    from sympy.diffgeom import Manifold, Patch, CoordSystem, BaseScalarField, Differential
    from sympy.diffgeom.rn import R2
    x,y = symbols('x y', real=True)
    m = Manifold('M', 2)
    assert latex(m) == r'\text{M}'
    p = Patch('P', m)
    assert latex(p) == r'\text{P}_{\text{M}}'
    rect = CoordSystem('rect', p, [x, y])
    assert latex(rect) == r'\text{rect}^{\text{P}}_{\text{M}}'
    b = BaseScalarField(rect, 0)
    assert latex(b) == r'\mathbf{x}'

    g = Function('g')
    s_field = g(R2.x, R2.y)
    assert latex(Differential(s_field)) == \
        r'\operatorname{d}\left(g{\left(\mathbf{x},\mathbf{y} \right)}\right)'

