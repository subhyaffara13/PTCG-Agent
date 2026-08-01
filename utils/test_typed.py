
def test_typed():
    class A(Basic):
        pass

    class B(Basic):
        pass

    rmzeros = rm_id(lambda x: x == S(0))
    rmones = rm_id(lambda x: x == S(1))
    remove_something = typed({A: rmzeros, B: rmones})

    assert remove_something(A(S(0), S(1))) == A(S(1))
    assert remove_something(B(S(0), S(1))) == B(S(0))

