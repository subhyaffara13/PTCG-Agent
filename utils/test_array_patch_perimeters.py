
def test_array_patch_perimeters():
    # This compares the old implementation as a reference for the
    # vectorized one.
    def check(x, rstride, cstride):
        rows, cols = x.shape
        row_inds = [*range(0, rows-1, rstride), rows-1]
        col_inds = [*range(0, cols-1, cstride), cols-1]
        polys = []
        for rs, rs_next in itertools.pairwise(row_inds):
            for cs, cs_next in itertools.pairwise(col_inds):
                # +1 ensures we share edges between polygons
                ps = cbook._array_perimeter(x[rs:rs_next+1, cs:cs_next+1]).T
                polys.append(ps)
        polys = np.asarray(polys)
        assert np.array_equal(polys,
                              cbook._array_patch_perimeters(
                                  x, rstride=rstride, cstride=cstride))

    def divisors(n):
        return [i for i in range(1, n + 1) if n % i == 0]

    for rows, cols in [(5, 5), (7, 14), (13, 9)]:
        x = np.arange(rows * cols).reshape(rows, cols)
        for rstride, cstride in itertools.product(divisors(rows - 1),
                                                  divisors(cols - 1)):
            check(x, rstride=rstride, cstride=cstride)

