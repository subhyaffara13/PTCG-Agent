
def test_upretty_sub_super():
    assert upretty( Symbol('beta_1_2') ) == 'β₁ ₂'
    assert upretty( Symbol('beta^1^2') ) == 'β¹ ²'
    assert upretty( Symbol('beta_1^2') ) == 'β²₁'
    assert upretty( Symbol('beta_10_20') ) == 'β₁₀ ₂₀'
    assert upretty( Symbol('beta_ax_gamma^i') ) == 'βⁱₐₓ ᵧ'
    assert upretty( Symbol("F^1^2_3_4") ) == 'F¹ ²₃ ₄'
    assert upretty( Symbol("F_1_2^3^4") ) == 'F³ ⁴₁ ₂'
    assert upretty( Symbol("F_1_2_3_4") ) == 'F₁ ₂ ₃ ₄'
    assert upretty( Symbol("F^1^2^3^4") ) == 'F¹ ² ³ ⁴'

