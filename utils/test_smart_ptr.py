
def test_smart_ptr(capture):
    # Object1
    for i, o in enumerate(
        [m.make_object_1(), m.make_object_2(), m.MyObject1(3)], start=1
    ):
        assert o.getRefCount() == 1
        with capture:
            m.print_object_1(o)
            m.print_object_2(o)
            m.print_object_3(o)
            m.print_object_4(o)
        assert capture == f"MyObject1[{i}]\n" * 4

    for i, o in enumerate(
        [m.make_myobject1_1(), m.make_myobject1_2(), m.MyObject1(6), 7], start=4
    ):
        print(o)
        with capture:
            if not isinstance(o, int):
                m.print_object_1(o)
                m.print_object_2(o)
                m.print_object_3(o)
                m.print_object_4(o)
            m.print_myobject1_1(o)
            m.print_myobject1_2(o)
            m.print_myobject1_3(o)
            m.print_myobject1_4(o)

        times = 4 if isinstance(o, int) else 8
        assert capture == f"MyObject1[{i}]\n" * times

    cstats = ConstructorStats.get(m.MyObject1)
    assert cstats.alive() == 0
    expected_values = [f"MyObject1[{i}]" for i in range(1, 7)] + ["MyObject1[7]"] * 4
    assert cstats.values() == expected_values
    assert cstats.default_constructions == 0
    assert cstats.copy_constructions == 0
    # assert cstats.move_constructions >= 0 # Doesn't invoke any
    assert cstats.copy_assignments == 0
    assert cstats.move_assignments == 0

    # Object2
    for i, o in zip(
        [8, 6, 7], [m.MyObject2(8), m.make_myobject2_1(), m.make_myobject2_2()]
    ):
        print(o)
        with capture:
            m.print_myobject2_1(o)
            m.print_myobject2_2(o)
            m.print_myobject2_3(o)
            m.print_myobject2_4(o)
        assert capture == f"MyObject2[{i}]\n" * 4

    cstats = ConstructorStats.get(m.MyObject2)
    assert cstats.alive() == 1
    o = None
    assert cstats.alive() == 0
    assert cstats.values() == ["MyObject2[8]", "MyObject2[6]", "MyObject2[7]"]
    assert cstats.default_constructions == 0
    assert cstats.copy_constructions == 0
    # assert cstats.move_constructions >= 0 # Doesn't invoke any
    assert cstats.copy_assignments == 0
    assert cstats.move_assignments == 0

    # Object3
    for i, o in zip(
        [9, 8, 9], [m.MyObject3(9), m.make_myobject3_1(), m.make_myobject3_2()]
    ):
        print(o)
        with capture:
            m.print_myobject3_1(o)
            m.print_myobject3_2(o)
            m.print_myobject3_3(o)
            m.print_myobject3_4(o)
        assert capture == f"MyObject3[{i}]\n" * 4

    cstats = ConstructorStats.get(m.MyObject3)
    assert cstats.alive() == 1
    o = None
    assert cstats.alive() == 0
    assert cstats.values() == ["MyObject3[9]", "MyObject3[8]", "MyObject3[9]"]
    assert cstats.default_constructions == 0
    assert cstats.copy_constructions == 0
    # assert cstats.move_constructions >= 0 # Doesn't invoke any
    assert cstats.copy_assignments == 0
    assert cstats.move_assignments == 0

    # Object
    cstats = ConstructorStats.get(m.Object)
    assert cstats.alive() == 0
    assert cstats.values() == []
    assert cstats.default_constructions == 10
    assert cstats.copy_constructions == 0
    # assert cstats.move_constructions >= 0 # Doesn't invoke any
    assert cstats.copy_assignments == 0
    assert cstats.move_assignments == 0

    # ref<>
    cstats = m.cstats_ref()
    assert cstats.alive() == 0
    assert cstats.values() == ["from pointer"] * 10
    assert cstats.default_constructions == 30
    assert cstats.copy_constructions == 12
    # assert cstats.move_constructions >= 0 # Doesn't invoke any
    assert cstats.copy_assignments == 30
    assert cstats.move_assignments == 0

