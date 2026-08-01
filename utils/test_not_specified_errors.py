
def test_not_specified_errors():
    """This test will cover errors that arise from trying to access attributes
    that were not specified upon object creation or were specified on creation
    and the user tries to recalculate them."""
    # Trying to access form 2 when form 1 given
    # Trying to access form 3 when form 2 given

    symsystem1 = SymbolicSystem(states, comb_explicit_rhs)

    with raises(AttributeError):
        symsystem1.comb_implicit_mat
    with raises(AttributeError):
        symsystem1.comb_implicit_rhs
    with raises(AttributeError):
        symsystem1.dyn_implicit_mat
    with raises(AttributeError):
        symsystem1.dyn_implicit_rhs
    with raises(AttributeError):
        symsystem1.kin_explicit_rhs
    with raises(AttributeError):
        symsystem1.compute_explicit_form()

    symsystem2 = SymbolicSystem(coordinates, comb_implicit_rhs, speeds=speeds,
                                mass_matrix=comb_implicit_mat)

    with raises(AttributeError):
        symsystem2.dyn_implicit_mat
    with raises(AttributeError):
        symsystem2.dyn_implicit_rhs
    with raises(AttributeError):
        symsystem2.kin_explicit_rhs

    # Attribute error when trying to access coordinates and speeds when only the
    # states were given.
    with raises(AttributeError):
        symsystem1.coordinates
    with raises(AttributeError):
        symsystem1.speeds

    # Attribute error when trying to access bodies and loads when they are not
    # given
    with raises(AttributeError):
        symsystem1.bodies
    with raises(AttributeError):
        symsystem1.loads

    # Attribute error when trying to access comb_explicit_rhs before it was
    # calculated
    with raises(AttributeError):
        symsystem2.comb_explicit_rhs

