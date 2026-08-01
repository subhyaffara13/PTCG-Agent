
def _assert_hasattr(a, b, msg=None):
    if msg is None:
        msg = f'{a} does not have attribute {b}'
    assert_(hasattr(a, b), msg=msg)

