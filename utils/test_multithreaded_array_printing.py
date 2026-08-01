
def test_multithreaded_array_printing():
    # the dragon4 implementation uses a static scratch space for performance
    # reasons this test makes sure it is set up in a thread-safe manner

    run_threaded(TestPrintOptions().test_floatmode, 500)

