
def check_dimensions(expr, unit_system="SI"):
    """Return expr if units in addends have the same
    base dimensions, else raise a ValueError."""
    # the case of adding a number to a dimensional quantity
    # is ignored for the sake of SymPy core routines, so this
    # function will raise an error now if such an addend is
    # found.
    # Also, when doing substitutions, multiplicative constants
    # might be introduced, so remove those now

    from sympy.physics.units import UnitSystem
    unit_system = UnitSystem.get_unit_system(unit_system)

    def addDict(dict1, dict2):
        """Merge dictionaries by adding values of common keys and
        removing keys with value of 0."""
        dict3 = {**dict1, **dict2}
        for key, value in dict3.items():
            if key in dict1 and key in dict2:
                dict3[key] = value + dict1[key]
        return {key:val for key, val in dict3.items() if val != 0}

    adds = expr.atoms(Add)
    DIM_OF = unit_system.get_dimension_system().get_dimensional_dependencies
    for a in adds:
        deset = set()
        for ai in a.args:
            if ai.is_number:
                deset.add(())
                continue
            dims = []
            skip = False
            dimdict = {}
            for i in Mul.make_args(ai):
                if i.has(Quantity):
                    i = Dimension(unit_system.get_dimensional_expr(i))
                if i.has(Dimension):
                    dimdict = addDict(dimdict, DIM_OF(i))
                elif i.free_symbols:
                    skip = True
                    break
            dims.extend(dimdict.items())
            if not skip:
                deset.add(tuple(sorted(dims, key=default_sort_key)))
                if len(deset) > 1:
                    raise ValueError(
                        "addends have incompatible dimensions: {}".format(deset))

    # clear multiplicative constants on Dimensions which may be
    # left after substitution
    reps = {}
    for m in expr.atoms(Mul):
        if any(isinstance(i, Dimension) for i in m.args):
            reps[m] = m.func(*[
                i for i in m.args if not i.is_number])

    return expr.xreplace(reps)

