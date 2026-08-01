
def test_multiple_inheritance_python():
    class MI1(m.Base1, m.Base2):
        def __init__(self, i, j):
            m.Base1.__init__(self, i)
            m.Base2.__init__(self, j)

    class B1:
        def v(self):
            return 1

    class MI2(B1, m.Base1, m.Base2):
        def __init__(self, i, j):
            B1.__init__(self)
            m.Base1.__init__(self, i)
            m.Base2.__init__(self, j)

    class MI3(MI2):
        def __init__(self, i, j):
            MI2.__init__(self, i, j)

    class MI4(MI3, m.Base2):
        def __init__(self, i, j):
            MI3.__init__(self, i, j)
            # This should be ignored (Base2 is already initialized via MI2):
            m.Base2.__init__(self, i + 100)

    class MI5(m.Base2, B1, m.Base1):
        def __init__(self, i, j):
            B1.__init__(self)
            m.Base1.__init__(self, i)
            m.Base2.__init__(self, j)

    class MI6(m.Base2, B1):
        def __init__(self, i):
            m.Base2.__init__(self, i)
            B1.__init__(self)

    class B2(B1):
        def v(self):
            return 2

    class B3:
        def v(self):
            return 3

    class B4(B3, B2):
        def v(self):
            return 4

    class MI7(B4, MI6):
        def __init__(self, i):
            B4.__init__(self)
            MI6.__init__(self, i)

    class MI8(MI6, B3):
        def __init__(self, i):
            MI6.__init__(self, i)
            B3.__init__(self)

    class MI8b(B3, MI6):
        def __init__(self, i):
            B3.__init__(self)
            MI6.__init__(self, i)

    mi1 = MI1(1, 2)
    assert mi1.foo() == 1
    assert mi1.bar() == 2

    mi2 = MI2(3, 4)
    assert mi2.v() == 1
    assert mi2.foo() == 3
    assert mi2.bar() == 4

    mi3 = MI3(5, 6)
    assert mi3.v() == 1
    assert mi3.foo() == 5
    assert mi3.bar() == 6

    mi4 = MI4(7, 8)
    assert mi4.v() == 1
    assert mi4.foo() == 7
    assert mi4.bar() == 8

    mi5 = MI5(10, 11)
    assert mi5.v() == 1
    assert mi5.foo() == 10
    assert mi5.bar() == 11

    mi6 = MI6(12)
    assert mi6.v() == 1
    assert mi6.bar() == 12

    mi7 = MI7(13)
    assert mi7.v() == 4
    assert mi7.bar() == 13

    mi8 = MI8(14)
    assert mi8.v() == 1
    assert mi8.bar() == 14

    mi8b = MI8b(15)
    assert mi8b.v() == 3
    assert mi8b.bar() == 15

