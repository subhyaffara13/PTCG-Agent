
def test_pretty_ImageSet():
    imgset = ImageSet(Lambda((x, y), x + y), {1, 2, 3}, {3, 4})
    ascii_str = '{x + y | x in {1, 2, 3}, y in {3, 4}}'
    ucode_str = '{x + y │ x ∊ {1, 2, 3}, y ∊ {3, 4}}'
    assert pretty(imgset) == ascii_str
    assert upretty(imgset) == ucode_str

    imgset = ImageSet(Lambda(((x, y),), x + y), ProductSet({1, 2, 3}, {3, 4}))
    ascii_str = '{x + y | (x, y) in {1, 2, 3} x {3, 4}}'
    ucode_str = '{x + y │ (x, y) ∊ {1, 2, 3} × {3, 4}}'
    assert pretty(imgset) == ascii_str
    assert upretty(imgset) == ucode_str

    imgset = ImageSet(Lambda(x, x**2), S.Naturals)
    ascii_str = '''\
  2                 \n\
{x  | x in Naturals}'''
    ucode_str = '''\
⎧ 2 │      ⎫\n\
⎨x  │ x ∊ ℕ⎬\n\
⎩   │      ⎭'''
    assert pretty(imgset) == ascii_str
    assert upretty(imgset) == ucode_str

    # TODO: The "x in N" parts below should be centered independently of the
    # 1/x**2 fraction
    imgset = ImageSet(Lambda(x, 1/x**2), S.Naturals)
    ascii_str = '''\
 1                  \n\
{-- | x in Naturals}
  2                 \n\
 x                  '''
    ucode_str = '''\
⎧1  │      ⎫\n\
⎪── │ x ∊ ℕ⎪\n\
⎨ 2 │      ⎬\n\
⎪x  │      ⎪\n\
⎩   │      ⎭'''
    assert pretty(imgset) == ascii_str
    assert upretty(imgset) == ucode_str

    imgset = ImageSet(Lambda((x, y), 1/(x + y)**2), S.Naturals, S.Naturals)
    ascii_str = '''\
    1                                    \n\
{-------- | x in Naturals, y in Naturals}
        2                                \n\
 (x + y)                                 '''
    ucode_str = '''\
⎧   1     │             ⎫
⎪──────── │ x ∊ ℕ, y ∊ ℕ⎪
⎨       2 │             ⎬
⎪(x + y)  │             ⎪
⎩         │             ⎭'''
    assert pretty(imgset) == ascii_str
    assert upretty(imgset) == ucode_str

    # issue 23449 centering issue
    assert upretty([Symbol("ihat") / (Symbol("i") + 1)]) == '''\
⎡  î  ⎤
⎢─────⎥
⎣i + 1⎦\
'''
    assert upretty(Matrix([Symbol("ihat"), Symbol("i") + 1])) == '''\
⎡  î  ⎤
⎢     ⎥
⎣i + 1⎦\
'''

