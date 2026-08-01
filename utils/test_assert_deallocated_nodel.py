
def test_assert_deallocated_nodel():
    class C:
        pass
    with pytest.raises(ReferenceError):
        # Need to delete after using if in with-block context
        # Note: assert_deallocated(C) needs to be assigned for the test
        # to function correctly.  It is assigned to _, but _ itself is
        # not referenced in the body of the with, it is only there for
        # the refcount.
        with assert_deallocated(C) as _:
            pass

