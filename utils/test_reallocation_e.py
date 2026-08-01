
def test_reallocation_e(capture, msg):
    with capture:
        create_and_destroy(3.5, 4.5)
    assert msg(capture) == strip_comments(
        """
        noisy new               # preallocation needed before invoking placement-new overload
        noisy placement new     # Placement new
        NoisyAlloc(double 3.5)  # construction
        ---
        ~NoisyAlloc()  # Destructor
        noisy delete   # operator delete
    """
    )

