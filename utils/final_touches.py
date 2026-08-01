
def final_touches(s2, r, deg_g):
    """
    s2 is sylvester2, r is the row pointer in s2,
    deg_g is the degree of the poly last inserted in s2.

    After a gcd of degree > 0 has been found with Van Vleck's
    method, and was inserted into s2, if its last term is not
    in the last column of s2, then it is inserted as many
    times as needed, rotated right by one each time, until
    the condition is met.

    """
    R = s2.row(r-1)

    # find the first non zero term
    for i in range(s2.cols):
        if R[0,i] == 0:
            continue
        else:
            break

    # missing rows until last term is in last column
    mr = s2.cols - (i + deg_g + 1)

    # insert them by replacing the existing entries in the row
    i = 0
    while mr != 0 and r + i < s2.rows :
        s2[r + i, : ] = rotate_r(R, i + 1)
        i += 1
        mr -= 1

    return s2

