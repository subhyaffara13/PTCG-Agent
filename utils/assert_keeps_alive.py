
def assert_keeps_alive(cl, method, *args):
    cstats = ConstructorStats.get(cl)
    start_with = cstats.alive()
    a = cl()
    assert cstats.alive() == start_with + 1
    z = method(a, *args)
    assert cstats.alive() == start_with + 1
    del a
    # Here's the keep alive in action:
    assert cstats.alive() == start_with + 1
    del z
    # Keep alive should have expired:
    assert cstats.alive() == start_with

