
def test_reallocation_d(capture, msg):
    with capture:
        create_and_destroy(2.5, 3)
    assert msg(capture) == strip_comments(
        """
        NoisyAlloc(double 2.5)  # construction (local func variable: operator_new not called)
        noisy new               # return-by-value "new" part 1: allocation
        ~NoisyAlloc()           # moved-away local func variable destruction
        ---
        ~NoisyAlloc()  # Destructor
        noisy delete   # operator delete
    """
    )

