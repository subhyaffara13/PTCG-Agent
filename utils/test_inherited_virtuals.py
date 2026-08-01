
def test_inherited_virtuals():
    class AR(m.A_Repeat):
        def unlucky_number(self):
            return 99

    class AT(m.A_Tpl):
        def unlucky_number(self):
            return 999

    obj = AR()
    assert obj.say_something(3) == "hihihi"
    assert obj.unlucky_number() == 99
    assert obj.say_everything() == "hi 99"

    obj = AT()
    assert obj.say_something(3) == "hihihi"
    assert obj.unlucky_number() == 999
    assert obj.say_everything() == "hi 999"

    for obj in [m.B_Repeat(), m.B_Tpl()]:
        assert obj.say_something(3) == "B says hi 3 times"
        assert obj.unlucky_number() == 13
        assert obj.lucky_number() == 7.0
        assert obj.say_everything() == "B says hi 1 times 13"

    for obj in [m.C_Repeat(), m.C_Tpl()]:
        assert obj.say_something(3) == "B says hi 3 times"
        assert obj.unlucky_number() == 4444
        assert obj.lucky_number() == 888.0
        assert obj.say_everything() == "B says hi 1 times 4444"

    class CR(m.C_Repeat):
        def lucky_number(self):
            return m.C_Repeat.lucky_number(self) + 1.25

    obj = CR()
    assert obj.say_something(3) == "B says hi 3 times"
    assert obj.unlucky_number() == 4444
    assert obj.lucky_number() == 889.25
    assert obj.say_everything() == "B says hi 1 times 4444"

    class CT(m.C_Tpl):
        pass

    obj = CT()
    assert obj.say_something(3) == "B says hi 3 times"
    assert obj.unlucky_number() == 4444
    assert obj.lucky_number() == 888.0
    assert obj.say_everything() == "B says hi 1 times 4444"

    class CCR(CR):
        def lucky_number(self):
            return CR.lucky_number(self) * 10

    obj = CCR()
    assert obj.say_something(3) == "B says hi 3 times"
    assert obj.unlucky_number() == 4444
    assert obj.lucky_number() == 8892.5
    assert obj.say_everything() == "B says hi 1 times 4444"

    class CCT(CT):
        def lucky_number(self):
            return CT.lucky_number(self) * 1000

    obj = CCT()
    assert obj.say_something(3) == "B says hi 3 times"
    assert obj.unlucky_number() == 4444
    assert obj.lucky_number() == 888000.0
    assert obj.say_everything() == "B says hi 1 times 4444"

    class DR(m.D_Repeat):
        def unlucky_number(self):
            return 123

        def lucky_number(self):
            return 42.0

    for obj in [m.D_Repeat(), m.D_Tpl()]:
        assert obj.say_something(3) == "B says hi 3 times"
        assert obj.unlucky_number() == 4444
        assert obj.lucky_number() == 888.0
        assert obj.say_everything() == "B says hi 1 times 4444"

    obj = DR()
    assert obj.say_something(3) == "B says hi 3 times"
    assert obj.unlucky_number() == 123
    assert obj.lucky_number() == 42.0
    assert obj.say_everything() == "B says hi 1 times 123"

    class DT(m.D_Tpl):
        def say_something(self, times):
            return "DT says:" + (" quack" * times)

        def unlucky_number(self):
            return 1234

        def lucky_number(self):
            return -4.25

    obj = DT()
    assert obj.say_something(3) == "DT says: quack quack quack"
    assert obj.unlucky_number() == 1234
    assert obj.lucky_number() == -4.25
    assert obj.say_everything() == "DT says: quack 1234"

    class DT2(DT):
        def say_something(self, times):
            return "DT2: " + ("QUACK" * times)

        def unlucky_number(self):
            return -3

    class BT(m.B_Tpl):
        def say_something(self, times):
            return "BT" * times

        def unlucky_number(self):
            return -7

        def lucky_number(self):
            return -1.375

    obj = BT()
    assert obj.say_something(3) == "BTBTBT"
    assert obj.unlucky_number() == -7
    assert obj.lucky_number() == -1.375
    assert obj.say_everything() == "BT -7"

