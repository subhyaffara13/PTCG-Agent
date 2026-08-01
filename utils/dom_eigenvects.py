
def dom_eigenvects(A, l=Dummy('lambda')):
    charpoly = A.charpoly()
    rows, cols = A.shape
    domain = A.domain
    _, factors = dup_factor_list(charpoly, domain)

    rational_eigenvects = []
    algebraic_eigenvects = []
    for base, exp in factors:
        if len(base) == 2:
            field = domain
            eigenval = -base[1] / base[0]

            EE_items = [
                [eigenval if i == j else field.zero for j in range(cols)]
                for i in range(rows)]
            EE = DomainMatrix(EE_items, (rows, cols), field)

            basis = (A - EE).nullspace(divide_last=True)
            rational_eigenvects.append((field, eigenval, exp, basis))
        else:
            minpoly = Poly.from_list(base, l, domain=domain)
            field = FiniteExtension(minpoly)
            eigenval = field(l)

            AA_items = [
                [Poly.from_list([item], l, domain=domain).rep for item in row]
                for row in A.rep.to_ddm()]
            AA_items = [[field(item) for item in row] for row in AA_items]
            AA = DomainMatrix(AA_items, (rows, cols), field)
            EE_items = [
                [eigenval if i == j else field.zero for j in range(cols)]
                for i in range(rows)]
            EE = DomainMatrix(EE_items, (rows, cols), field)

            basis = (AA - EE).nullspace(divide_last=True)
            algebraic_eigenvects.append((field, minpoly, exp, basis))

    return rational_eigenvects, algebraic_eigenvects

