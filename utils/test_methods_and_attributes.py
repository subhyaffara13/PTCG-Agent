
def test_methods_and_attributes():
    instance1 = m.ExampleMandA()
    instance2 = m.ExampleMandA(32)

    instance1.add1(instance2)
    instance1.add2(instance2)
    instance1.add3(instance2)
    instance1.add4(instance2)
    instance1.add5(instance2)
    instance1.add6(32)
    instance1.add7(32)
    instance1.add8(32)
    instance1.add9(32)
    instance1.add10(32)

    assert str(instance1) == "ExampleMandA[value=320]"
    assert str(instance2) == "ExampleMandA[value=32]"
    assert str(instance1.self1()) == "ExampleMandA[value=320]"
    assert str(instance1.self2()) == "ExampleMandA[value=320]"
    assert str(instance1.self3()) == "ExampleMandA[value=320]"
    assert str(instance1.self4()) == "ExampleMandA[value=320]"
    assert str(instance1.self5()) == "ExampleMandA[value=320]"

    assert instance1.internal1() == 320
    assert instance1.internal2() == 320
    assert instance1.internal3() == 320
    assert instance1.internal4() == 320
    assert instance1.internal5() == 320

    assert instance1.overloaded() == "()"
    assert instance1.overloaded(0) == "(int)"
    assert instance1.overloaded(1, 1.0) == "(int, float)"
    assert instance1.overloaded(2.0, 2) == "(float, int)"
    assert instance1.overloaded(3, 3) == "(int, int)"
    assert instance1.overloaded(4.0, 4.0) == "(float, float)"
    assert instance1.overloaded_const(-3) == "(int) const"
    assert instance1.overloaded_const(5, 5.0) == "(int, float) const"
    assert instance1.overloaded_const(6.0, 6) == "(float, int) const"
    assert instance1.overloaded_const(7, 7) == "(int, int) const"
    assert instance1.overloaded_const(8.0, 8.0) == "(float, float) const"
    assert instance1.overloaded_float(1, 1) == "(float, float)"
    assert instance1.overloaded_float(1, 1.0) == "(float, float)"
    assert instance1.overloaded_float(1.0, 1) == "(float, float)"
    assert instance1.overloaded_float(1.0, 1.0) == "(float, float)"

    assert instance1.value == 320
    instance1.value = 100
    assert str(instance1) == "ExampleMandA[value=100]"

    cstats = ConstructorStats.get(m.ExampleMandA)
    assert cstats.alive() == 2
    del instance1, instance2
    assert cstats.alive() == 0
    assert cstats.values() == ["32"]
    assert cstats.default_constructions == 1
    assert cstats.copy_constructions == 2
    assert cstats.move_constructions >= 2
    assert cstats.copy_assignments == 0
    assert cstats.move_assignments == 0

