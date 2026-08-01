
def test_capsule(capture):
    pytest.gc_collect()
    with capture:
        a = m.return_capsule_with_destructor()
        del a
        pytest.gc_collect()
    assert (
        capture.unordered
        == """
        creating capsule
        destructing capsule
    """
    )

    with capture:
        a = m.return_renamed_capsule_with_destructor()
        del a
        pytest.gc_collect()
    assert (
        capture.unordered
        == """
        creating capsule
        renaming capsule
        destructing capsule
    """
    )

    with capture:
        a = m.return_capsule_with_destructor_2()
        del a
        pytest.gc_collect()
    assert (
        capture.unordered
        == """
        creating capsule
        destructing capsule: 1234
    """
    )

    with capture:
        a = m.return_capsule_with_destructor_3()
        del a
        pytest.gc_collect()
    assert (
        capture.unordered
        == """
        creating capsule
        destructing capsule: 1233
        original name: oname
    """
    )

    with capture:
        a = m.return_renamed_capsule_with_destructor_2()
        del a
        pytest.gc_collect()
    assert (
        capture.unordered
        == """
        creating capsule
        renaming capsule
        destructing capsule: 1234
    """
    )

    with capture:
        a = m.return_capsule_with_name_and_destructor()
        del a
        pytest.gc_collect()
    assert (
        capture.unordered
        == """
        created capsule (1234, 'pointer type description')
        destructing capsule (1234, 'pointer type description')
    """
    )

    with capture:
        a = m.return_capsule_with_explicit_nullptr_dtor()
        del a
        pytest.gc_collect()
    assert (
        capture.unordered
        == """
        creating capsule with explicit nullptr dtor
    """
    )

