
def test_multiple_inheritance_python_many_bases():
    class MIMany14(m.BaseN1, m.BaseN2, m.BaseN3, m.BaseN4):
        def __init__(self):
            m.BaseN1.__init__(self, 1)
            m.BaseN2.__init__(self, 2)
            m.BaseN3.__init__(self, 3)
            m.BaseN4.__init__(self, 4)

    class MIMany58(m.BaseN5, m.BaseN6, m.BaseN7, m.BaseN8):
        def __init__(self):
            m.BaseN5.__init__(self, 5)
            m.BaseN6.__init__(self, 6)
            m.BaseN7.__init__(self, 7)
            m.BaseN8.__init__(self, 8)

    class MIMany916(
        m.BaseN9,
        m.BaseN10,
        m.BaseN11,
        m.BaseN12,
        m.BaseN13,
        m.BaseN14,
        m.BaseN15,
        m.BaseN16,
    ):
        def __init__(self):
            m.BaseN9.__init__(self, 9)
            m.BaseN10.__init__(self, 10)
            m.BaseN11.__init__(self, 11)
            m.BaseN12.__init__(self, 12)
            m.BaseN13.__init__(self, 13)
            m.BaseN14.__init__(self, 14)
            m.BaseN15.__init__(self, 15)
            m.BaseN16.__init__(self, 16)

    class MIMany19(MIMany14, MIMany58, m.BaseN9):
        def __init__(self):
            MIMany14.__init__(self)
            MIMany58.__init__(self)
            m.BaseN9.__init__(self, 9)

    class MIMany117(MIMany14, MIMany58, MIMany916, m.BaseN17):
        def __init__(self):
            MIMany14.__init__(self)
            MIMany58.__init__(self)
            MIMany916.__init__(self)
            m.BaseN17.__init__(self, 17)

    # Inherits from 4 registered C++ classes: can fit in one pointer on any modern arch:
    a = MIMany14()
    for i in range(1, 4):
        assert getattr(a, "f" + str(i))() == 2 * i

    # Inherits from 8: requires 1/2 pointers worth of holder flags on 32/64-bit arch:
    b = MIMany916()
    for i in range(9, 16):
        assert getattr(b, "f" + str(i))() == 2 * i

    # Inherits from 9: requires >= 2 pointers worth of holder flags
    c = MIMany19()
    for i in range(1, 9):
        assert getattr(c, "f" + str(i))() == 2 * i

    # Inherits from 17: requires >= 3 pointers worth of holder flags
    d = MIMany117()
    for i in range(1, 17):
        assert getattr(d, "f" + str(i))() == 2 * i

