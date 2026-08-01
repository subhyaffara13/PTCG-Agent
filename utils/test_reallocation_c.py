
def test_reallocation_c(capture, msg):
    with capture:
        create_and_destroy(2, 3)
    assert msg(capture) == strip_comments(
        """
        noisy new          # pointer factory calling "new", allocation
        NoisyAlloc(int 2)  # constructor
        ---
        ~NoisyAlloc()  # Destructor
        noisy delete   # operator delete
    """
    )

