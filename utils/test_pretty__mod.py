
def test_pretty_Mod():
    from sympy.core import Mod

    ascii_str1 = "x mod 7"
    ucode_str1 = "x mod 7"

    ascii_str2 = "(x + 1) mod 7"
    ucode_str2 = "(x + 1) mod 7"

    ascii_str3 = "2*x mod 7"
    ucode_str3 = "2⋅x mod 7"

    ascii_str4 = "(x mod 7) + 1"
    ucode_str4 = "(x mod 7) + 1"

    ascii_str5 = "2*(x mod 7)"
    ucode_str5 = "2⋅(x mod 7)"

    x = symbols('x', integer=True)
    assert pretty(Mod(x, 7)) == ascii_str1
    assert upretty(Mod(x, 7)) == ucode_str1
    assert pretty(Mod(x + 1, 7)) == ascii_str2
    assert upretty(Mod(x + 1, 7)) == ucode_str2
    assert pretty(Mod(2 * x, 7)) == ascii_str3
    assert upretty(Mod(2 * x, 7)) == ucode_str3
    assert pretty(Mod(x, 7) + 1) == ascii_str4
    assert upretty(Mod(x, 7) + 1) == ucode_str4
    assert pretty(2 * Mod(x, 7)) == ascii_str5
    assert upretty(2 * Mod(x, 7)) == ucode_str5

