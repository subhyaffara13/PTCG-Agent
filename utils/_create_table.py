
def _create_table(
    shards: list[tuple[tuple[int, int], tuple[int, int], int]], device_kind: str = ""
):
    """
    Creates a tabulate table given row and column ranges with device name
    """
    from tabulate import tabulate

    # Extract unique row and column ranges
    row_ranges = sorted({block[0] for block in shards})
    col_ranges = sorted({block[1] for block in shards})

    # Create a matrix initialized with empty strings
    matrix = [["" for _ in col_ranges] for _ in row_ranges]

    # Fill the matrix with values
    for block in shards:
        row_index = row_ranges.index(block[0])
        col_index = col_ranges.index(block[1])
        if matrix[row_index][col_index] == "":
            matrix[row_index][col_index] = device_kind + ":" + str(block[2])
        else:
            matrix[row_index][col_index] += "," + str(block[2])

    # Prepare headers
    row_headers = [f"Row {r[0]}-{r[1]}" for r in row_ranges]
    col_headers = [f"Col {c[0]}-{c[1]}" for c in col_ranges]

    return tabulate(matrix, headers=col_headers, showindex=row_headers)


def _create_table(table, domain=QQ):
    """
    Creates the look-up table. For a similar implementation
    see meijerint._create_lookup_table.
    """

    def add(formula, annihilator, arg, x0=0, y0=()):
        """
        Adds a formula in the dictionary
        """
        table.setdefault(_mytype(formula, x_1), []).append((formula,
            HolonomicFunction(annihilator, arg, x0, y0)))

    R = domain.old_poly_ring(x_1)
    _, Dx = DifferentialOperators(R, 'Dx')

    # add some basic functions
    add(sin(x_1), Dx**2 + 1, x_1, 0, [0, 1])
    add(cos(x_1), Dx**2 + 1, x_1, 0, [1, 0])
    add(exp(x_1), Dx - 1, x_1, 0, 1)
    add(log(x_1), Dx + x_1*Dx**2, x_1, 1, [0, 1])

    add(erf(x_1), 2*x_1*Dx + Dx**2, x_1, 0, [0, 2/sqrt(pi)])
    add(erfc(x_1), 2*x_1*Dx + Dx**2, x_1, 0, [1, -2/sqrt(pi)])
    add(erfi(x_1), -2*x_1*Dx + Dx**2, x_1, 0, [0, 2/sqrt(pi)])

    add(sinh(x_1), Dx**2 - 1, x_1, 0, [0, 1])
    add(cosh(x_1), Dx**2 - 1, x_1, 0, [1, 0])

    add(sinc(x_1), x_1 + 2*Dx + x_1*Dx**2, x_1)

    add(Si(x_1), x_1*Dx + 2*Dx**2 + x_1*Dx**3, x_1)
    add(Ci(x_1), x_1*Dx + 2*Dx**2 + x_1*Dx**3, x_1)

    add(Shi(x_1), -x_1*Dx + 2*Dx**2 + x_1*Dx**3, x_1)

