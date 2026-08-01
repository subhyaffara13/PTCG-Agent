
def test_upper_hessenberg_decomposition():
    A = Matrix([
        [1, 0, sqrt(3)],
        [sqrt(2), Rational(1, 2), 2],
        [1, Rational(1, 4), 3],
    ])
    H, P = A.upper_hessenberg_decomposition()
    assert simplify(P * P.H) == eye(P.cols)
    assert simplify(P.H * P) == eye(P.cols)
    assert H.is_upper_hessenberg
    assert (simplify(P * H * P.H)) == A


    B = Matrix([
        [1, 2, 10],
        [8, 2, 5],
        [3, 12, 34],
    ])
    H, P = B.upper_hessenberg_decomposition()
    assert simplify(P * P.H) == eye(P.cols)
    assert simplify(P.H * P) == eye(P.cols)
    assert H.is_upper_hessenberg
    assert simplify(P * H * P.H) == B

    C = Matrix([
        [1, sqrt(2), 2, 3],
        [0, 5, 3, 4],
        [1, 1, 4, sqrt(5)],
        [0, 2, 2, 3]
    ])

    H, P = C.upper_hessenberg_decomposition()
    assert simplify(P * P.H) == eye(P.cols)
    assert simplify(P.H * P) == eye(P.cols)
    assert H.is_upper_hessenberg
    assert simplify(P * H * P.H) == C

    D = Matrix([
        [1, 2, 3],
        [-3, 5, 6],
        [4, -8, 9],
    ])
    H, P = D.upper_hessenberg_decomposition()
    assert simplify(P * P.H) == eye(P.cols)
    assert simplify(P.H * P) == eye(P.cols)
    assert H.is_upper_hessenberg
    assert simplify(P * H * P.H) == D

    E = Matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [1, 1, 0, 1],
        [1, 1, 1, 0]
    ])

    H, P = E.upper_hessenberg_decomposition()
    assert simplify(P * P.H) == eye(P.cols)
    assert simplify(P.H * P) == eye(P.cols)
    assert H.is_upper_hessenberg
    assert simplify(P * H * P.H) == E

