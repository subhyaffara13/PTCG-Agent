
def check_may_share_memory_exact(a, b):
    got = np.may_share_memory(a, b, max_work=MAY_SHARE_EXACT)

    assert_equal(np.may_share_memory(a, b),
                 np.may_share_memory(a, b, max_work=MAY_SHARE_BOUNDS))

    a.fill(0)
    b.fill(0)
    a.fill(1)
    exact = b.any()

    err_msg = ""
    if got != exact:
        base_delta = a.__array_interface__['data'][0] - b.__array_interface__['data'][0]
        err_msg = "    " + "\n    ".join([
            f"base_a - base_b = {base_delta!r}",
            f"shape_a = {a.shape!r}",
            f"shape_b = {b.shape!r}",
            f"strides_a = {a.strides!r}",
            f"strides_b = {b.strides!r}",
            f"size_a = {a.size!r}",
            f"size_b = {b.size!r}"
        ])

    assert_equal(got, exact, err_msg=err_msg)

