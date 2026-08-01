
def test_issue_20113():
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x = Symbol('x')

    # verify the capability to use custom backends
    plot(sin(x), backend=Plot, show=False)
    p2 = plot(sin(x), backend=MatplotlibBackend, show=False)
    assert p2.backend == MatplotlibBackend
    assert len(p2[0].get_data()[0]) >= 30
    p3 = plot(sin(x), backend=DummyBackendOk, show=False)
    assert p3.backend == DummyBackendOk
    assert len(p3[0].get_data()[0]) >= 30

    # test for an improper coded backend
    p4 = plot(sin(x), backend=DummyBackendNotOk, show=False)
    assert p4.backend == DummyBackendNotOk
    assert len(p4[0].get_data()[0]) >= 30
    with raises(NotImplementedError):
        p4.show()
    with raises(NotImplementedError):
        p4.save("test/path")
    with raises(NotImplementedError):
        p4._backend.close()

