
def test_reallocation_g(capture, msg):
    with capture:
        create_and_destroy(5, "hi")
    assert msg(capture) == strip_comments(
        """
        noisy new            # preallocation needed before invoking first placement new
        noisy delete         # delete before considering new-style constructor
        noisy new            # preallocation for second placement new
        noisy placement new  # Placement new in the second placement new overload
        NoisyAlloc(int 5)    # construction
        ---
        ~NoisyAlloc()  # Destructor
        noisy delete   # operator delete
    """
    )

