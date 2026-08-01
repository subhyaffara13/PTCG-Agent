
def test_apply_beta_to_alpha_route():
    APPLY = apply_beta_to_alpha_route

    # indicates empty alpha-chain with attached beta-rule #bidx
    def Q(bidx):
        return (set(), [bidx])

    # x -> a        &(a,b) -> x     --  x -> a
    A = {'x': {'a'}}
    B = [(And('a', 'b'), 'x')]
    assert APPLY(A, B) == {'x': ({'a'}, []), 'a': Q(0), 'b': Q(0)}

    # x -> a        &(a,!x) -> b    --  x -> a
    A = {'x': {'a'}}
    B = [(And('a', Not('x')), 'b')]
    assert APPLY(A, B) == {'x': ({'a'}, []), Not('x'): Q(0), 'a': Q(0)}

    # x -> a b      &(a,b) -> c     --  x -> a b c
    A = {'x': {'a', 'b'}}
    B = [(And('a', 'b'), 'c')]
    assert APPLY(A, B) == \
        {'x': ({'a', 'b', 'c'}, []), 'a': Q(0), 'b': Q(0)}

    # x -> a        &(a,b) -> y     --  x -> a [#0]
    A = {'x': {'a'}}
    B = [(And('a', 'b'), 'y')]
    assert APPLY(A, B) == {'x': ({'a'}, [0]), 'a': Q(0), 'b': Q(0)}

    # x -> a b c    &(a,b) -> c     --  x -> a b c
    A = {'x': {'a', 'b', 'c'}}
    B = [(And('a', 'b'), 'c')]
    assert APPLY(A, B) == \
        {'x': ({'a', 'b', 'c'}, []), 'a': Q(0), 'b': Q(0)}

    # x -> a b      &(a,b,c) -> y   --  x -> a b [#0]
    A = {'x': {'a', 'b'}}
    B = [(And('a', 'b', 'c'), 'y')]
    assert APPLY(A, B) == \
        {'x': ({'a', 'b'}, [0]), 'a': Q(0), 'b': Q(0), 'c': Q(0)}

    # x -> a b      &(a,b) -> c     --  x -> a b c d
    # c -> d                            c -> d
    A = {'x': {'a', 'b'}, 'c': {'d'}}
    B = [(And('a', 'b'), 'c')]
    assert APPLY(A, B) == {'x': ({'a', 'b', 'c', 'd'}, []),
        'c': ({'d'}, []), 'a': Q(0), 'b': Q(0)}

    # x -> a b      &(a,b) -> c     --  x -> a b c d e
    # c -> d        &(c,d) -> e         c -> d e
    A = {'x': {'a', 'b'}, 'c': {'d'}}
    B = [(And('a', 'b'), 'c'), (And('c', 'd'), 'e')]
    assert APPLY(A, B) == {'x': ({'a', 'b', 'c', 'd', 'e'}, []),
        'c': ({'d', 'e'}, []), 'a': Q(0), 'b': Q(0), 'd': Q(1)}

    # x -> a b      &(a,y) -> z     --  x -> a b y z
    #               &(a,b) -> y
    A = {'x': {'a', 'b'}}
    B = [(And('a', 'y'), 'z'), (And('a', 'b'), 'y')]
    assert APPLY(A, B) == {'x': ({'a', 'b', 'y', 'z'}, []),
        'a': (set(), [0, 1]), 'y': Q(0), 'b': Q(1)}

    # x -> a b      &(a,!b) -> c    --  x -> a b
    A = {'x': {'a', 'b'}}
    B = [(And('a', Not('b')), 'c')]
    assert APPLY(A, B) == \
        {'x': ({'a', 'b'}, []), 'a': Q(0), Not('b'): Q(0)}

    # !x -> !a !b   &(!a,b) -> c    --  !x -> !a !b
    A = {Not('x'): {Not('a'), Not('b')}}
    B = [(And(Not('a'), 'b'), 'c')]
    assert APPLY(A, B) == \
        {Not('x'): ({Not('a'), Not('b')}, []), Not('a'): Q(0), 'b': Q(0)}

    # x -> a b      &(b,c) -> !a    --  x -> a b
    A = {'x': {'a', 'b'}}
    B = [(And('b', 'c'), Not('a'))]
    assert APPLY(A, B) == {'x': ({'a', 'b'}, []), 'b': Q(0), 'c': Q(0)}

    # x -> a b      &(a, b) -> c    --  x -> a b c p
    # c -> p a
    A = {'x': {'a', 'b'}, 'c': {'p', 'a'}}
    B = [(And('a', 'b'), 'c')]
    assert APPLY(A, B) == {'x': ({'a', 'b', 'c', 'p'}, []),
        'c': ({'p', 'a'}, []), 'a': Q(0), 'b': Q(0)}

