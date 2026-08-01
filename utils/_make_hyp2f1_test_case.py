
def _make_hyp2f1_test_case(a, b, c, z, rtol):
    """Generate string for single test case as used in test_hyp2f1.py."""
    expected = mp_hyp2f1(a, b, c, z)
    return (
        "    pytest.param(\n"
        "        Hyp2f1TestCase(\n"
        f"            a={a},\n"
        f"            b={b},\n"
        f"            c={c},\n"
        f"            z={z},\n"
        f"            expected={expected},\n"
        f"            rtol={rtol},\n"
        "        ),\n"
        "    ),"
    )

