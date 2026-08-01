
def subresultants_vv(p, q, x, method = 0):
    """
    p, q are polynomials in Z[x] (intended) or Q[x]. It is assumed
    that degree(p, x) >= degree(q, x).

    Computes the subresultant prs of p, q by triangularizing,
    in Z[x] or in Q[x], all the smaller matrices encountered in the
    process of triangularizing sylvester2, Sylvester's matrix of 1853;
    see references 1 and 2 for Van Vleck's method. With each remainder,
    sylvester2 gets updated and is prepared to be printed if requested.

    If sylvester2 has small dimensions and you want to see the final,
    triangularized matrix use this version with method=1; otherwise,
    use either this version with method=0 (default) or the faster version,
    subresultants_vv_2(p, q, x), where sylvester2 is used implicitly.

    Sylvester's matrix sylvester1  is also used to compute one
    subresultant per remainder; namely, that of the leading
    coefficient, in order to obtain the correct sign and to
    force the remainder coefficients to become subresultants.

    If the subresultant prs is complete, then it coincides with the
    Euclidean sequence of the polynomials p, q.

    If the final, triangularized matrix s2 is printed, then:
        (a) if deg(p) - deg(q) > 1 or deg( gcd(p, q) ) > 0, several
            of the last rows in s2 will remain unprocessed;
        (b) if deg(p) - deg(q) == 0, p will not appear in the final matrix.

    References
    ==========
    1. Akritas, A. G.: ``A new method for computing polynomial greatest
    common divisors and polynomial remainder sequences.''
    Numerische MatheMatik 52, 119-127, 1988.

    2. Akritas, A. G., G.I. Malaschonok and P.S. Vigklas: ``On a Theorem
    by Van Vleck Regarding Sturm Sequences.''
    Serdica Journal of Computing, 7, No 4, 101-134, 2013.

    3. Akritas, A. G.:``Three New Methods for Computing Subresultant
    Polynomial Remainder Sequences (PRS's).'' Serdica Journal of Computing 9(1) (2015), 1-26.

    """
    # make sure neither p nor q is 0
    if p == 0 or q == 0:
        return [p, q]

    # make sure proper degrees
    f, g = p, q
    n = deg_f = degree(f, x)
    m = deg_g = degree(g, x)
    if n == 0 and m == 0:
        return [f, g]
    if n < m:
        n, m, deg_f, deg_g, f, g = m, n, deg_g, deg_f, g, f
    if n > 0 and m == 0:
        return [f, g]

    # initialize
    s1 = sylvester(f, g, x, 1)
    s2 = sylvester(f, g, x, 2)
    sr_list = [f, g]
    col_num = 2 * n         # columns in s2

    # make two rows (row0, row1) of poly coefficients
    row0 = Poly(f, x, domain = QQ).all_coeffs()
    leng0 = len(row0)
    for i in range(col_num - leng0):
        row0.append(0)
    row0 = Matrix([row0])
    row1 = Poly(g,x, domain = QQ).all_coeffs()
    leng1 = len(row1)
    for i in range(col_num - leng1):
        row1.append(0)
    row1 = Matrix([row1])

    # row pointer for deg_f - deg_g == 1; may be reset below
    r = 2

    # modify first rows of s2 matrix depending on poly degrees
    if deg_f - deg_g > 1:
        r = 1
        # replacing the existing entries in the rows of s2,
        # insert row0 (deg_f - deg_g - 1) times, rotated each time
        for i in range(deg_f - deg_g - 1):
            s2[r + i, : ] = rotate_r(row0, i + 1)
        r = r + deg_f - deg_g - 1
        # insert row1 (deg_f - deg_g) times, rotated each time
        for i in range(deg_f - deg_g):
            s2[r + i, : ] = rotate_r(row1, r + i)
        r = r + deg_f - deg_g

    if deg_f - deg_g == 0:
        r = 0

    # main loop
    while deg_g > 0:
        # create a small matrix M, and triangularize it;
        M = create_ma(deg_f, deg_g, row1, row0, col_num)
        # will need only the first and last rows of M
        for i in range(deg_f - deg_g + 1):
            M1 = pivot(M, i, i)
            M = M1[:, :]

        # treat last row of M as poly; find its degree
        d = find_degree(M, deg_f)
        if d is None:
            break
        exp_deg = deg_g - 1

        # evaluate one determinant & make coefficients subresultants
        sign_value = correct_sign(n, m, s1, exp_deg, exp_deg - d)
        poly = row2poly(M[M.rows - 1, :], d, x)
        temp2 = LC(poly, x)
        poly = simplify((poly / temp2) * sign_value)

        # update s2 by inserting first row of M as needed
        row0 = M[0, :]
        for i in range(deg_g - d):
            s2[r + i, :] = rotate_r(row0, r + i)
        r = r + deg_g - d

        # update s2 by inserting last row of M as needed
        row1 = rotate_l(M[M.rows - 1, :], deg_f - d)
        row1 = (row1 / temp2) * sign_value
        for i in range(deg_g - d):
            s2[r + i, :] = rotate_r(row1, r + i)
        r = r + deg_g - d

        # update degrees
        deg_f, deg_g = deg_g, d

        # append poly with subresultant coeffs
        sr_list.append(poly)

    # final touches to print the s2 matrix
    if method != 0 and s2.rows > 2:
        s2 = final_touches(s2, r, deg_g)
        pprint(s2)
    elif method != 0 and s2.rows == 2:
        s2[1, :] = rotate_r(s2.row(1), 1)
        pprint(s2)

    return sr_list

