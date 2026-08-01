
def constexpr_next_power_of_2(
    n: tl.constexpr, *, _builder: object = None
) -> tl.constexpr:
    """
    A version triton.next_power_of_two that can be used within a kernel on constants.
    """
    assert isinstance(n, tl.constexpr)
    return tl.constexpr(triton.next_power_of_2(n.value))

