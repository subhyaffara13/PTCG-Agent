
def test_reallocation_f(capture, msg):
    with capture:
        create_and_destroy(4, 0.5)
    assert msg(capture) == strip_comments(
        """
        noisy new          # preallocation needed before invoking placement-new overload
        noisy delete       # deallocation of preallocated storage
        noisy new          # Factory pointer allocation
        NoisyAlloc(int 4)  # factory pointer construction
        ---
        ~NoisyAlloc()  # Destructor
        noisy delete   # operator delete
    """
    )

