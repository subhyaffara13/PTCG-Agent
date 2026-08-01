
def test_upretty_subs_missing_in_24():
    assert upretty( Symbol('F_beta') ) == 'Fᵦ'
    assert upretty( Symbol('F_gamma') ) == 'Fᵧ'
    assert upretty( Symbol('F_rho') ) == 'Fᵨ'
    assert upretty( Symbol('F_phi') ) == 'Fᵩ'
    assert upretty( Symbol('F_chi') ) == 'Fᵪ'

    assert upretty( Symbol('F_a') ) == 'Fₐ'
    assert upretty( Symbol('F_e') ) == 'Fₑ'
    assert upretty( Symbol('F_i') ) == 'Fᵢ'
    assert upretty( Symbol('F_o') ) == 'Fₒ'
    assert upretty( Symbol('F_u') ) == 'Fᵤ'
    assert upretty( Symbol('F_r') ) == 'Fᵣ'
    assert upretty( Symbol('F_v') ) == 'Fᵥ'
    assert upretty( Symbol('F_x') ) == 'Fₓ'

