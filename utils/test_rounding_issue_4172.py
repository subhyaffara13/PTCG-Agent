
def test_rounding_issue_4172():
    assert int((E**100).round()) == \
        26881171418161354484126255515800135873611119
    assert int((pi**100).round()) == \
        51878483143196131920862615246303013562686760680406
    assert int((Rational(1)/EulerGamma**100).round()) == \
        734833795660954410469466

