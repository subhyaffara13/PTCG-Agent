
def test_missing_in_2X_issue_9047():
    assert upretty( Symbol('F_h') ) == 'Fₕ'
    assert upretty( Symbol('F_k') ) == 'Fₖ'
    assert upretty( Symbol('F_l') ) == 'Fₗ'
    assert upretty( Symbol('F_m') ) == 'Fₘ'
    assert upretty( Symbol('F_n') ) == 'Fₙ'
    assert upretty( Symbol('F_p') ) == 'Fₚ'
    assert upretty( Symbol('F_s') ) == 'Fₛ'
    assert upretty( Symbol('F_t') ) == 'Fₜ'

