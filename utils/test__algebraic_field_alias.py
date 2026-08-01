
def test_AlgebraicField_alias():
    # No default alias:
    k = QQ.algebraic_field(sqrt(2))
    assert k.ext.alias is None

    # For a single extension, its alias is used:
    alpha = AlgebraicNumber(sqrt(2), alias='alpha')
    k = QQ.algebraic_field(alpha)
    assert k.ext.alias.name == 'alpha'

    # Can override the alias of a single extension:
    k = QQ.algebraic_field(alpha, alias='theta')
    assert k.ext.alias.name == 'theta'

    # With multiple extensions, no default alias:
    k = QQ.algebraic_field(sqrt(2), sqrt(3))
    assert k.ext.alias is None

    # With multiple extensions, no default alias, even if one of
    # the extensions has one:
    k = QQ.algebraic_field(alpha, sqrt(3))
    assert k.ext.alias is None

    # With multiple extensions, may set an alias:
    k = QQ.algebraic_field(sqrt(2), sqrt(3), alias='theta')
    assert k.ext.alias.name == 'theta'

    # Alias is passed to constructed field elements:
    k = QQ.algebraic_field(alpha)
    beta = k.to_alg_num(k([1, 2, 3]))
    assert beta.alias is alpha.alias

