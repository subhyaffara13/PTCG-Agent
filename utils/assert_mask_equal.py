
def assertMaskEqual(testcase, m1, m2, msg=None):
    """Checks to see if the 2 given masks are equal."""
    m1_count = m1.count()

    testcase.assertEqual(m1.get_size(), m2.get_size(), msg=msg)
    testcase.assertEqual(m1_count, m2.count(), msg=msg)
    testcase.assertEqual(m1_count, m1.overlap_area(m2, (0, 0)), msg=msg)


def assert_mask_equal(m1, m2, err_msg=''):
    """
    Asserts the equality of two masks.

    """
    if m1 is nomask:
        assert_(m2 is nomask)
    if m2 is nomask:
        assert_(m1 is nomask)
    assert_array_equal(m1, m2, err_msg=err_msg)

