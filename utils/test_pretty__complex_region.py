
def test_pretty_ComplexRegion():
    from sympy.sets.fancysets import ComplexRegion
    cregion = ComplexRegion(Interval(3, 5)*Interval(4, 6))
    ascii_str = '{x + y*I | x, y in [3, 5] x [4, 6]}'
    ucode_str = '{x + y⋅ⅈ │ x, y ∊ [3, 5] × [4, 6]}'
    assert pretty(cregion) == ascii_str
    assert upretty(cregion) == ucode_str

    cregion = ComplexRegion(Interval(0, 1)*Interval(0, 2*pi), polar=True)
    ascii_str = '{r*(I*sin(theta) + cos(theta)) | r, theta in [0, 1] x [0, 2*pi)}'
    ucode_str = '{r⋅(ⅈ⋅sin(θ) + cos(θ)) │ r, θ ∊ [0, 1] × [0, 2⋅π)}'
    assert pretty(cregion) == ascii_str
    assert upretty(cregion) == ucode_str

    cregion = ComplexRegion(Interval(3, 1/a**2)*Interval(4, 6))
    ascii_str = '''\
                       1            \n\
{x + y*I | x, y in [3, --] x [4, 6]}
                        2           \n\
                       a            '''
    ucode_str = '''\
⎧        │        ⎡   1 ⎤         ⎫
⎪x + y⋅ⅈ │ x, y ∊ ⎢3, ──⎥ × [4, 6]⎪
⎨        │        ⎢    2⎥         ⎬
⎪        │        ⎣   a ⎦         ⎪
⎩        │                        ⎭'''
    assert pretty(cregion) == ascii_str
    assert upretty(cregion) == ucode_str

    cregion = ComplexRegion(Interval(0, 1/a**2)*Interval(0, 2*pi), polar=True)
    ascii_str = '''\
                                                 1               \n\
{r*(I*sin(theta) + cos(theta)) | r, theta in [0, --] x [0, 2*pi)}
                                                  2              \n\
                                                 a               '''
    ucode_str = '''\
⎧                      │        ⎡   1 ⎤           ⎫
⎪r⋅(ⅈ⋅sin(θ) + cos(θ)) │ r, θ ∊ ⎢0, ──⎥ × [0, 2⋅π)⎪
⎨                      │        ⎢    2⎥           ⎬
⎪                      │        ⎣   a ⎦           ⎪
⎩                      │                          ⎭'''
    assert pretty(cregion) == ascii_str
    assert upretty(cregion) == ucode_str

