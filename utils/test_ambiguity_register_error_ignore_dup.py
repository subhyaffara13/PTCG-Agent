
def test_ambiguity_register_error_ignore_dup():
    f = Dispatcher('f')

    class A:
        pass
    class B(A):
        pass
    class C(A):
        pass

    # suppress warning for registering ambiguous signal
    f.add((A, B), lambda x,y: None, ambiguity_register_error_ignore_dup)
    f.add((B, A), lambda x,y: None, ambiguity_register_error_ignore_dup)
    f.add((A, C), lambda x,y: None, ambiguity_register_error_ignore_dup)
    f.add((C, A), lambda x,y: None, ambiguity_register_error_ignore_dup)

    # raises error if ambiguous signal is passed
    assert raises(NotImplementedError, lambda: f(B(), C()))

