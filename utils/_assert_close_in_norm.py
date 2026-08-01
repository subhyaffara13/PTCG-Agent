
def _assert_close_in_norm(x, y, rtol, size, rdt):
    # helper function for testing
    err_msg = f"size: {size}  rdt: {rdt}"
    assert_array_less(np.linalg.norm(x - y), rtol*np.linalg.norm(x), err_msg)


def _assert_close_in_norm(x, y, rtol, size, rdt):
    # helper function for testing
    err_msg = f"size: {size}  rdt: {rdt}"
    assert_array_less(np.linalg.norm(x - y), rtol*np.linalg.norm(x), err_msg)

