
def test_While():
    x = symbols('x')
    assert fcode(While(abs(x) > 1, [aug_assign(x, '-', 1)]), source_format='free') == (
        'do while (abs(x) > 1)\n'
        '   x = x - 1\n'
        'end do'
    )


def test_While():
    xpp = AddAugmentedAssignment(x, 1)
    whl1 = While(x < 2, [xpp])
    assert whl1.condition.args[0] == x
    assert whl1.condition.args[1] == 2
    assert whl1.condition == Lt(x, 2, evaluate=False)
    assert whl1.body.args == (xpp,)
    assert whl1.func(*whl1.args) == whl1

    cblk = CodeBlock(AddAugmentedAssignment(x, 1))
    whl2 = While(x < 2, cblk)
    assert whl1 == whl2
    assert whl1 != While(x < 3, [xpp])

