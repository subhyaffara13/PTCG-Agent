
def test_upretty_modifiers():
    # Accents
    assert upretty( Symbol('Fmathring') ) == 'F̊'
    assert upretty( Symbol('Fddddot') ) == 'F⃜'
    assert upretty( Symbol('Fdddot') ) == 'F⃛'
    assert upretty( Symbol('Fddot') ) == 'F̈'
    assert upretty( Symbol('Fdot') ) == 'Ḟ'
    assert upretty( Symbol('Fcheck') ) == 'F̌'
    assert upretty( Symbol('Fbreve') ) == 'F̆'
    assert upretty( Symbol('Facute') ) == 'F́'
    assert upretty( Symbol('Fgrave') ) == 'F̀'
    assert upretty( Symbol('Ftilde') ) == 'F̃'
    assert upretty( Symbol('Fhat') ) == 'F̂'
    assert upretty( Symbol('Fbar') ) == 'F̅'
    assert upretty( Symbol('Fvec') ) == 'F⃗'
    assert upretty( Symbol('Fprime') ) == 'F′'
    assert upretty( Symbol('Fprm') ) == 'F′'
    # No faces are actually implemented, but test to make sure the modifiers are stripped
    assert upretty( Symbol('Fbold') ) == 'Fbold'
    assert upretty( Symbol('Fbm') ) == 'Fbm'
    assert upretty( Symbol('Fcal') ) == 'Fcal'
    assert upretty( Symbol('Fscr') ) == 'Fscr'
    assert upretty( Symbol('Ffrak') ) == 'Ffrak'
    # Brackets
    assert upretty( Symbol('Fnorm') ) == '‖F‖'
    assert upretty( Symbol('Favg') ) == '⟨F⟩'
    assert upretty( Symbol('Fabs') ) == '|F|'
    assert upretty( Symbol('Fmag') ) == '|F|'
    # Combinations
    assert upretty( Symbol('xvecdot') ) == 'x⃗̇'
    assert upretty( Symbol('xDotVec') ) == 'ẋ⃗'
    assert upretty( Symbol('xHATNorm') ) == '‖x̂‖'
    assert upretty( Symbol('xMathring_yCheckPRM__zbreveAbs') ) == 'x̊_y̌′__|z̆|'
    assert upretty( Symbol('alphadothat_nVECDOT__tTildePrime') ) == 'α̇̂_n⃗̇__t̃′'
    assert upretty( Symbol('x_dot') ) == 'x_dot'
    assert upretty( Symbol('x__dot') ) == 'x__dot'

