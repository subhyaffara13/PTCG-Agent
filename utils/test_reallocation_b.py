
def test_reallocation_b(capture, msg):
    with capture:
        create_and_destroy(1.5)
    assert msg(capture) == strip_comments(
        """
        noisy new               # allocation required to attempt first overload
        noisy delete            # have to dealloc before considering factory init overload
        noisy new               # pointer factory calling "new", part 1: allocation
        NoisyAlloc(double 1.5)  # ... part two, invoking constructor
        ---
        ~NoisyAlloc()  # Destructor
        noisy delete   # operator delete
    """
    )

