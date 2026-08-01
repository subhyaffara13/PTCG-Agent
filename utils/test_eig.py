
def test_eig():
    v = 0
    AS = []

    A = mp.matrix([[2, 1, 0],  # jordan block of size 3
                   [0, 2, 1],
                   [0, 0, 2]])
    AS.append(A)
    AS.append(A.transpose())

    A = mp.matrix([[2, 0, 0],  # jordan block of size 2
                   [0, 2, 1],
                   [0, 0, 2]])
    AS.append(A)
    AS.append(A.transpose())

    A = mp.matrix([[2, 0, 1],  # jordan block of size 2
                   [0, 2, 0],
                   [0, 0, 2]])
    AS.append(A)
    AS.append(A.transpose())

    A=  mp.matrix([[0, 0, 1],  # cyclic
                   [1, 0, 0],
                   [0, 1, 0]])
    AS.append(A)
    AS.append(A.transpose())

    for A in AS:
        run_hessenberg(A, verbose = v)
        run_schur(A, verbose = v)
        run_eig(A, verbose = v)

