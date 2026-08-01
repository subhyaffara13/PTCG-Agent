
def test_random_sample():
    alist = list(range(100))

    assert list(random_sample(prob=1, seq=alist, random_state=2016)) == alist

    mk_rsample = lambda rs=1: list(random_sample(prob=0.1,
                                                 seq=alist,
                                                 random_state=rs))
    rsample1 = mk_rsample()
    assert rsample1 == mk_rsample()

    rsample2 = mk_rsample(1984)
    randobj = Random(1984)
    assert rsample2 == mk_rsample(randobj)

    assert rsample1 != rsample2

    assert mk_rsample(hash(object)) == mk_rsample(hash(object))
    assert mk_rsample(hash(object)) != mk_rsample(hash(object()))
    assert mk_rsample(b"a") == mk_rsample("a")

    assert raises(TypeError, lambda: mk_rsample([]))

