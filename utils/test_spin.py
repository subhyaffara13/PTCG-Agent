
def test_spin():
    assert operators_to_state({J2Op, JxOp}) == JxKet
    assert operators_to_state({J2Op, JyOp}) == JyKet
    assert operators_to_state({J2Op, JzOp}) == JzKet
    assert operators_to_state({J2Op(), JxOp()}) == JxKet
    assert operators_to_state({J2Op(), JyOp()}) == JyKet
    assert operators_to_state({J2Op(), JzOp()}) == JzKet

    assert state_to_operators(JxKet) == {J2Op, JxOp}
    assert state_to_operators(JyKet) == {J2Op, JyOp}
    assert state_to_operators(JzKet) == {J2Op, JzOp}
    assert state_to_operators(JxBra) == {J2Op, JxOp}
    assert state_to_operators(JyBra) == {J2Op, JyOp}
    assert state_to_operators(JzBra) == {J2Op, JzOp}

    assert state_to_operators(JxKet(S.Half, S.Half)) == {J2Op(), JxOp()}
    assert state_to_operators(JyKet(S.Half, S.Half)) == {J2Op(), JyOp()}
    assert state_to_operators(JzKet(S.Half, S.Half)) == {J2Op(), JzOp()}
    assert state_to_operators(JxBra(S.Half, S.Half)) == {J2Op(), JxOp()}
    assert state_to_operators(JyBra(S.Half, S.Half)) == {J2Op(), JyOp()}
    assert state_to_operators(JzBra(S.Half, S.Half)) == {J2Op(), JzOp()}


def test_spin():
    lz = JzOp('L')
    ket = JzKet(1, 0)
    bra = JzBra(1, 0)
    cket = JzKetCoupled(1, 0, (1, 2))
    cbra = JzBraCoupled(1, 0, (1, 2))
    cket_big = JzKetCoupled(1, 0, (1, 2, 3))
    cbra_big = JzBraCoupled(1, 0, (1, 2, 3))
    rot = Rotation(1, 2, 3)
    bigd = WignerD(1, 2, 3, 4, 5, 6)
    smalld = WignerD(1, 2, 3, 0, 4, 0)
    assert str(lz) == 'Lz'
    ascii_str = \
"""\
L \n\
 z\
"""
    ucode_str = \
"""\
L \n\
 z\
"""
    assert pretty(lz) == ascii_str
    assert upretty(lz) == ucode_str
    assert latex(lz) == 'L_z'
    sT(lz, "JzOp(Symbol('L'))")
    assert str(J2) == 'J2'
    ascii_str = \
"""\
 2\n\
J \
"""
    ucode_str = \
"""\
 2\n\
J \
"""
    assert pretty(J2) == ascii_str
    assert upretty(J2) == ucode_str
    assert latex(J2) == r'J^2'
    sT(J2, "J2Op(Symbol('J'))")
    assert str(Jz) == 'Jz'
    ascii_str = \
"""\
J \n\
 z\
"""
    ucode_str = \
"""\
J \n\
 z\
"""
    assert pretty(Jz) == ascii_str
    assert upretty(Jz) == ucode_str
    assert latex(Jz) == 'J_z'
    sT(Jz, "JzOp(Symbol('J'))")
    assert str(ket) == '|1,0>'
    assert pretty(ket) == '|1,0>'
    assert upretty(ket) == '❘1,0⟩'
    assert latex(ket) == r'{\left|1,0\right\rangle }'
    sT(ket, "JzKet(Integer(1),Integer(0))")
    assert str(bra) == '<1,0|'
    assert pretty(bra) == '<1,0|'
    assert upretty(bra) == '⟨1,0❘'
    assert latex(bra) == r'{\left\langle 1,0\right|}'
    sT(bra, "JzBra(Integer(1),Integer(0))")
    assert str(cket) == '|1,0,j1=1,j2=2>'
    assert pretty(cket) == '|1,0,j1=1,j2=2>'
    assert upretty(cket) == '❘1,0,j₁=1,j₂=2⟩'
    assert latex(cket) == r'{\left|1,0,j_{1}=1,j_{2}=2\right\rangle }'
    sT(cket, "JzKetCoupled(Integer(1),Integer(0),Tuple(Integer(1), Integer(2)),Tuple(Tuple(Integer(1), Integer(2), Integer(1))))")
    assert str(cbra) == '<1,0,j1=1,j2=2|'
    assert pretty(cbra) == '<1,0,j1=1,j2=2|'
    assert upretty(cbra) == '⟨1,0,j₁=1,j₂=2❘'
    assert latex(cbra) == r'{\left\langle 1,0,j_{1}=1,j_{2}=2\right|}'
    sT(cbra, "JzBraCoupled(Integer(1),Integer(0),Tuple(Integer(1), Integer(2)),Tuple(Tuple(Integer(1), Integer(2), Integer(1))))")
    assert str(cket_big) == '|1,0,j1=1,j2=2,j3=3,j(1,2)=3>'
    # TODO: Fix non-unicode pretty printing
    # i.e. j1,2 -> j(1,2)
    assert pretty(cket_big) == '|1,0,j1=1,j2=2,j3=3,j1,2=3>'
    assert upretty(cket_big) == '❘1,0,j₁=1,j₂=2,j₃=3,j₁,₂=3⟩'
    assert latex(cket_big) == \
        r'{\left|1,0,j_{1}=1,j_{2}=2,j_{3}=3,j_{1,2}=3\right\rangle }'
    sT(cket_big, "JzKetCoupled(Integer(1),Integer(0),Tuple(Integer(1), Integer(2), Integer(3)),Tuple(Tuple(Integer(1), Integer(2), Integer(3)), Tuple(Integer(1), Integer(3), Integer(1))))")
    assert str(cbra_big) == '<1,0,j1=1,j2=2,j3=3,j(1,2)=3|'
    assert pretty(cbra_big) == '<1,0,j1=1,j2=2,j3=3,j1,2=3|'
    assert upretty(cbra_big) == '⟨1,0,j₁=1,j₂=2,j₃=3,j₁,₂=3❘'
    assert latex(cbra_big) == \
        r'{\left\langle 1,0,j_{1}=1,j_{2}=2,j_{3}=3,j_{1,2}=3\right|}'
    sT(cbra_big, "JzBraCoupled(Integer(1),Integer(0),Tuple(Integer(1), Integer(2), Integer(3)),Tuple(Tuple(Integer(1), Integer(2), Integer(3)), Tuple(Integer(1), Integer(3), Integer(1))))")
    assert str(rot) == 'R(1,2,3)'
    assert pretty(rot) == 'R (1,2,3)'
    assert upretty(rot) == 'ℛ (1,2,3)'
    assert latex(rot) == r'\mathcal{R}\left(1,2,3\right)'
    sT(rot, "Rotation(Integer(1),Integer(2),Integer(3))")
    assert str(bigd) == 'WignerD(1, 2, 3, 4, 5, 6)'
    ascii_str = \
"""\
 1         \n\
D   (4,5,6)\n\
 2,3       \
"""
    ucode_str = \
"""\
 1         \n\
D   (4,5,6)\n\
 2,3       \
"""
    assert pretty(bigd) == ascii_str
    assert upretty(bigd) == ucode_str
    assert latex(bigd) == r'D^{1}_{2,3}\left(4,5,6\right)'
    sT(bigd, "WignerD(Integer(1), Integer(2), Integer(3), Integer(4), Integer(5), Integer(6))")
    assert str(smalld) == 'WignerD(1, 2, 3, 0, 4, 0)'
    ascii_str = \
"""\
 1     \n\
d   (4)\n\
 2,3   \
"""
    ucode_str = \
"""\
 1     \n\
d   (4)\n\
 2,3   \
"""
    assert pretty(smalld) == ascii_str
    assert upretty(smalld) == ucode_str
    assert latex(smalld) == r'd^{1}_{2,3}\left(4\right)'
    sT(smalld, "WignerD(Integer(1), Integer(2), Integer(3), Integer(0), Integer(4), Integer(0))")

