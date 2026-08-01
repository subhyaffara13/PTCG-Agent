
def test_mismatched_holder():
    import re

    with pytest.raises(RuntimeError) as excinfo:
        m.mismatched_holder_1()
    assert re.match(
        'generic_type: type ".*MismatchDerived1" does not have a non-default '
        'holder type while its base ".*MismatchBase1" does',
        str(excinfo.value),
    )

    with pytest.raises(RuntimeError) as excinfo:
        m.mismatched_holder_2()
    assert re.match(
        'generic_type: type ".*MismatchDerived2" has a non-default holder type '
        'while its base ".*MismatchBase2" does not',
        str(excinfo.value),
    )

