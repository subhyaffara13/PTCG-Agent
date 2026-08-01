
def test_issue_14041():
    import sympy.physics.mechanics as me

    A_frame = me.ReferenceFrame('A')
    thetad, phid = me.dynamicsymbols('theta, phi', 1)
    L = symbols('L')

    assert vlatex(L*(phid + thetad)**2*A_frame.x) == \
        r"L \left(\dot{\phi} + \dot{\theta}\right)^{2}\mathbf{\hat{a}_x}"
    assert vlatex((phid + thetad)**2*A_frame.x) == \
        r"\left(\dot{\phi} + \dot{\theta}\right)^{2}\mathbf{\hat{a}_x}"
    assert vlatex((phid*thetad)**a*A_frame.x) == \
        r"\left(\dot{\phi} \dot{\theta}\right)^{a}\mathbf{\hat{a}_x}"

