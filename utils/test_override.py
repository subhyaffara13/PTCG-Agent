
def test_override(capture, msg):
    class ExtendedExampleVirt(m.ExampleVirt):
        def __init__(self, state):
            super().__init__(state + 1)
            self.data = "Hello world"

        def run(self, value):
            print(f"ExtendedExampleVirt::run({value}), calling parent..")
            return super().run(value + 1)

        def run_bool(self):
            print("ExtendedExampleVirt::run_bool()")
            return False

        def get_string1(self):
            return "override1"

        def pure_virtual(self):
            print(f"ExtendedExampleVirt::pure_virtual(): {self.data}")

    class ExtendedExampleVirt2(ExtendedExampleVirt):
        def __init__(self, state):
            super().__init__(state + 1)

        def get_string2(self):
            return "override2"

    ex12 = m.ExampleVirt(10)
    with capture:
        assert m.runExampleVirt(ex12, 20) == 30
    assert (
        capture
        == """
        Original implementation of ExampleVirt::run(state=10, value=20, str1=default1, str2=default2)
    """
    )

    with pytest.raises(RuntimeError) as excinfo:
        m.runExampleVirtVirtual(ex12)
    assert (
        msg(excinfo.value)
        == 'Tried to call pure virtual function "ExampleVirt::pure_virtual"'
    )

    ex12p = ExtendedExampleVirt(10)
    with capture:
        assert m.runExampleVirt(ex12p, 20) == 32
    assert (
        capture
        == """
        ExtendedExampleVirt::run(20), calling parent..
        Original implementation of ExampleVirt::run(state=11, value=21, str1=override1, str2=default2)
    """
    )
    with capture:
        assert m.runExampleVirtBool(ex12p) is False
    assert capture == "ExtendedExampleVirt::run_bool()"
    with capture:
        m.runExampleVirtVirtual(ex12p)
    assert capture == "ExtendedExampleVirt::pure_virtual(): Hello world"

    ex12p2 = ExtendedExampleVirt2(15)
    with capture:
        assert m.runExampleVirt(ex12p2, 50) == 68
    assert (
        capture
        == """
        ExtendedExampleVirt::run(50), calling parent..
        Original implementation of ExampleVirt::run(state=17, value=51, str1=override1, str2=override2)
    """
    )

    cstats = ConstructorStats.get(m.ExampleVirt)
    assert cstats.alive() == 3
    del ex12, ex12p, ex12p2
    assert cstats.alive() == 0
    assert cstats.values() == ["10", "11", "17"]
    assert cstats.copy_constructions == 0
    assert cstats.move_constructions >= 0

