
def create_and_destroy(*args):
    a = m.NoisyAlloc(*args)
    print("---")
    del a
    pytest.gc_collect()

