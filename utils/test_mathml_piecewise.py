
def test_mathml_piecewise():
    from sympy.functions.elementary.piecewise import Piecewise
    # Content MathML
    assert mathml(Piecewise((x, x <= 1), (x**2, True))) == \
        '<piecewise><piece><ci>x</ci><apply><leq/><ci>x</ci><cn>1</cn></apply></piece><otherwise><apply><power/><ci>x</ci><cn>2</cn></apply></otherwise></piecewise>'

    raises(ValueError, lambda: mathml(Piecewise((x, x <= 1))))

