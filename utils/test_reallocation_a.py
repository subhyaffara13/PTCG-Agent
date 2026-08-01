
def test_reallocation_a(capture, msg):
    """When the constructor is overloaded, previous overloads can require a preallocated value.
    This test makes sure that such preallocated values only happen when they might be necessary,
    and that they are deallocated properly."""

    pytest.gc_collect()

    with capture:
        create_and_destroy(1)
    assert (
        msg(capture)
        == """
        noisy new
        noisy placement new
        NoisyAlloc(int 1)
        ---
        ~NoisyAlloc()
        noisy delete
    """
    )

