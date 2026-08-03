from typing import Dict

def test_any_object_in_sequence():
    # Cf. issue 5306
    b1 = Basic()
    b2 = Basic(Basic())

    expr = [b2, b1]
    assert pretty(expr) == "[Basic(Basic()), Basic()]"
    assert upretty(expr) == "[Basic(Basic()), Basic()]"

    expr = {b2, b1}
    assert pretty(expr) == "{Basic(), Basic(Basic())}"
    assert upretty(expr) == "{Basic(), Basic(Basic())}"

    expr = {b2: b1, b1: b2}
    expr2 = Dict({b2: b1, b1: b2})
    assert pretty(expr) == "{Basic(): Basic(Basic()), Basic(Basic()): Basic()}"
    assert pretty(
        expr2) == "{Basic(): Basic(Basic()), Basic(Basic()): Basic()}"
    assert upretty(
        expr) == "{Basic(): Basic(Basic()), Basic(Basic()): Basic()}"
    assert upretty(
        expr2) == "{Basic(): Basic(Basic()), Basic(Basic()): Basic()}"

