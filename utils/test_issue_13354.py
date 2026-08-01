
def test_issue_13354():
    """
    Test for proper pretty printing of physics vectors with ADD
    instances in arguments.

    Test is exactly the one suggested in the original bug report by
    @moorepants.
    """

    a, b, c = symbols('a, b, c')
    A = ReferenceFrame('A')
    v = a * A.x + b * A.y + c * A.z
    w = b * A.x + c * A.y + a * A.z
    z = w + v

    expected = """(a + b) a_x + (b + c) a_y + (a + c) a_z"""

    assert ascii_vpretty(z) == expected

