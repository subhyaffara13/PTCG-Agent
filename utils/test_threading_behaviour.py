
def test_threading_behaviour():
    # Test if the API is thread-safe.
    # This verifies if the lock mechanism and the use of `PyErr_Occurred`
    # is correct.
    errors = {"err1": None, "err2": None}

    class Distribution:
        def __init__(self, pdf_msg):
            self.pdf_msg = pdf_msg

        def pdf(self, x):
            if 49.9 < x < 50.0:
                raise ValueError(self.pdf_msg)
            return x

        def dpdf(self, x):
            return 1

    def func1():
        dist = Distribution('foo')
        rng = TransformedDensityRejection(dist, domain=(10, 100),
                                          random_state=12)
        try:
            rng.rvs(100000)
        except ValueError as e:
            errors['err1'] = e.args[0]

    def func2():
        dist = Distribution('bar')
        rng = TransformedDensityRejection(dist, domain=(10, 100),
                                          random_state=2)
        try:
            rng.rvs(100000)
        except ValueError as e:
            errors['err2'] = e.args[0]

    t1 = threading.Thread(target=func1)
    t2 = threading.Thread(target=func2)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    assert errors['err1'] == 'foo'
    assert errors['err2'] == 'bar'

